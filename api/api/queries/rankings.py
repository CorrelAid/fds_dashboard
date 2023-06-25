from sqlalchemy import func
from api.models import FoiRequest, PublicBody, Jurisdiction, Campaign, Message
from sqlalchemy import select, asc, desc, cast, Float, case, or_, nullslast


def to_dct(result):
    lst = []
    for row in result:
        dct = {}
        dct["name"] = str(row[0])
        dct["number"] = int(row[1])
        dct["resolution_rate"] = float(row[2])
        dct["number_overdue"] = int(row[3])
        dct["overdue_rate"] = float(row[4])
        successful = row[5]
        if successful is None:
            successful = 0
        dct["successful"] = float(successful)
        success_rate = row[6]
        if success_rate is None:
            success_rate = 0
        dct["success_rate"] = float(success_rate)
        lst.append(dct)

    return lst


def ranking(db):
    total_num = (
        select(FoiRequest.public_body_id, func.count(FoiRequest.id.distinct()))
        .where(FoiRequest.public_body_id is not None)
        .filter(or_(FoiRequest.campaign_id != 9, FoiRequest.campaign_id is None))
        .group_by(FoiRequest.public_body_id)
        .subquery()
    )

    resolved_mess = (
        select(Message.foi_request_id.distinct())
        .filter(Message.status.in_(["resolved", "partially_successful", "successful"]))
        .subquery()
    )

    resolved = (
        select(FoiRequest.public_body_id, func.count(FoiRequest.id.distinct()))
        .where(FoiRequest.public_body_id is not None)
        .filter(or_(FoiRequest.campaign_id != 9, FoiRequest.campaign_id is None))
        .filter(FoiRequest.id.in_(resolved_mess))
        .group_by(FoiRequest.public_body_id)
        .subquery()
    )

    successful = (
        select(FoiRequest.public_body_id, func.count(FoiRequest.id.distinct()))
        .where(FoiRequest.public_body_id is not None)
        .filter(or_(FoiRequest.campaign_id != 9, FoiRequest.campaign_id is None))
        .filter(FoiRequest.resolution.in_(["partially_successful", "successful"]))
        .group_by(FoiRequest.public_body_id)
        .subquery()
    )

    res_date = (
        select(Message.foi_request_id, func.min(Message.timestamp))
        .filter(Message.status.in_(["resolved", "partially_successful", "successful"]))
        .group_by(Message.foi_request_id)
        .subquery()
    )

    unres = (
        select(Message.foi_request_id, func.max(Message.timestamp))
        .filter(~Message.foi_request_id.in_(resolved_mess))
        .group_by(Message.foi_request_id)
        .subquery()
    )

    late_res = (
        select(FoiRequest.id)
        .join(res_date, FoiRequest.id == res_date.c.foi_request_id)
        .filter(or_(FoiRequest.campaign_id != 9, FoiRequest.campaign_id is None))
        .where(FoiRequest.due_date < res_date.c.min)
        .subquery()
    )

    late_unres = (
        select(FoiRequest.id)
        .join(unres, FoiRequest.id == unres.c.foi_request_id)
        .filter(or_(FoiRequest.campaign_id != 9, FoiRequest.campaign_id is None))
        .where(FoiRequest.due_date < unres.c.max)
        .subquery()
    )

    late_all = (
        select(func.coalesce(late_res.c.id, late_unres.c.id).label("id"))
        .join(late_unres, late_res.c.id == late_unres.c.id, full=True)
        .subquery()
    )

    late = (
        select(FoiRequest.public_body_id, func.count(late_all.c.id.distinct()))
        .join(late_all, FoiRequest.id == late_all.c.id, isouter=True)
        .group_by(FoiRequest.public_body_id)
        .subquery()
    )

    late2 = select(
        late.c.public_body_id, case((late.c.count.isnot(None), late.c.count), else_=0).label("count")
    ).subquery()

    return late2, total_num, resolved, successful


def ranking_public_body(db, s: str, ascending: bool):
    if ascending:
        ordering = asc
    else:
        ordering = desc
    late, total_num, resolved, successful = ranking(db)
    if s in ["Anzahl", "Erfolgsquote", "Verspätungsquote", "Abgeschlossenenquote", "Erfolgreich"]:
        stmt = (
            select(
                PublicBody.name,
                total_num.c.count.label("Anzahl"),
                (cast(resolved.c.count, Float) / total_num.c.count * 100).label("Abgeschlossenenquote"),
                late.c.count.label("Fristüberschreitungen"),
                (cast(late.c.count, Float) / total_num.c.count * 100).label("Verspätungsquote"),
                cast(successful.c.count, Float).label("Erfolgreich"),
                (cast(successful.c.count, Float) / total_num.c.count * 100).label("Erfolgsquote"),
            )
            .join(resolved, PublicBody.id == resolved.c.public_body_id)
            .join(total_num, PublicBody.id == total_num.c.public_body_id)
            .join(successful, PublicBody.id == successful.c.public_body_id, isouter=True)
            .join(late, late.c.public_body_id == PublicBody.id, isouter=True)
            .where(total_num.c.public_body_id == resolved.c.public_body_id)
            .where(total_num.c.count > 20)
            .order_by(nullslast(ordering(s)))
            .limit(10)
        )
    else:
        stmt = (
            select(
                PublicBody.name,
                total_num.c.count.label("Anzahl"),
                (cast(resolved.c.count, Float) / total_num.c.count * 100).label("Abgeschlossenenquote"),
                late.c.count.label("Fristüberschreitungen"),
                (cast(late.c.count, Float) / total_num.c.count * 100).label("Verspätungsquote"),
                successful.c.count.label("Erfolgreich"),
                (cast(successful.c.count, Float) / total_num.c.count * 100).label("Erfolgsquote"),
            )
            .join(resolved, PublicBody.id == resolved.c.public_body_id)
            .join(total_num, PublicBody.id == total_num.c.public_body_id)
            .join(late, late.c.public_body_id == PublicBody.id, isouter=True)
            .join(successful, PublicBody.id == successful.c.public_body_id, isouter=True)
            .where(total_num.c.public_body_id == resolved.c.public_body_id)
            .where(total_num.c.count > 20)
            .order_by(nullslast("Verspätungsquote"))
            .limit(10)
        )
    print(stmt)
    result = db.execute(stmt).fetchall()
    print(stmt)
    return to_dct(result)


def ranking_jurisdictions(db, s: str, ascending: bool):
    if ascending:
        ordering = asc
    else:
        ordering = desc

    late, total_num, resolved, successful = ranking(db)
    if s in ["Anzahl", "Erfolgsquote", "Verspätungsquote", "Abgeschlossenenquote", "Erfolgreich"]:
        stmt = (
            select(
                Jurisdiction.name,
                func.sum(total_num.c.count).label("Anzahl"),
                (cast(func.sum(resolved.c.count), Float) / func.sum(total_num.c.count) * 100).label(
                    "Abgeschlossenenquote"
                ),
                func.sum(late.c.count).label("Fristüberschreitungen"),
                (cast(func.sum(late.c.count), Float) / func.sum(total_num.c.count) * 100).label("Verspätungsquote"),
                func.sum(successful.c.count).label("Erfolgreich"),
                (cast(func.sum(successful.c.count), Float) / func.sum(total_num.c.count) * 100).label("Erfolgsquote"),
            )
            .join(PublicBody, Jurisdiction.id == PublicBody.jurisdiction_id)
            .join(resolved, PublicBody.id == resolved.c.public_body_id)
            .join(total_num, PublicBody.id == total_num.c.public_body_id)
            .join(late, late.c.public_body_id == PublicBody.id, isouter=True)
            .join(successful, PublicBody.id == successful.c.public_body_id, isouter=True)
            .where(total_num.c.public_body_id == resolved.c.public_body_id)
            .group_by(Jurisdiction.name)
            .order_by(nullslast(ordering(s)))
            .limit(10)
        )
    else:
        stmt = (
            select(
                Jurisdiction.name,
                func.sum(total_num.c.count).label("Anzahl"),
                (cast(func.sum(resolved.c.count), Float) / func.sum(total_num.c.count) * 100).label(
                    "Abgeschlossenenquote"
                ),
                func.sum(late.c.count).label("Fristüberschreitungen"),
                (cast(func.sum(late.c.count), Float) / func.sum(total_num.c.count) * 100).label("Verspätungsquote"),
                func.sum(successful.c.count).label("Erfolgreich"),
                (cast(func.sum(successful.c.count), Float) / func.sum(total_num.c.count) * 100).label("Erfolgsquote"),
            )
            .join(PublicBody, Jurisdiction.id == PublicBody.jurisdiction)
            .join(resolved, PublicBody.id == resolved.c.public_body_id)
            .join(total_num, PublicBody.id == total_num.c.public_body_id)
            .join(late, late.c.public_body_id == PublicBody.id, isouter=True)
            .join(successful, PublicBody.id == successful.c.public_body_id, isouter=True)
            .where(total_num.c.public_body_id == resolved.c.public_body_id)
            .group_by(Jurisdiction.name)
            .order_by(nullslast("Verspätungsquote"))
            .limit(10)
        )
    result = db.execute(stmt).fetchall()
    return to_dct(result)


def ranking_campaign(db, s: str, ascending: bool):
    total_num = (
        select(FoiRequest.campaign_id, func.count(FoiRequest.id.distinct())).group_by(FoiRequest.campaign_id).subquery()
    )

    resolved_mess = (
        select(Message.foi_request_id.distinct())
        .filter(Message.status.in_(["resolved", "partially_successful", "successful"]))
        .subquery()
    )

    resolved = (
        select(FoiRequest.campaign_id, func.count(FoiRequest.id.distinct()))
        .filter(FoiRequest.id.in_(resolved_mess))
        .group_by(FoiRequest.campaign_id)
        .subquery()
    )

    res_date = (
        select(Message.foi_request_id, func.min(Message.timestamp))
        .filter(Message.status.in_(["resolved", "partially_successful", "successful"]))
        .group_by(Message.foi_request_id)
        .subquery()
    )

    successful = (
        select(FoiRequest.campaign_id, func.count(FoiRequest.id.distinct()))
        .filter(FoiRequest.resolution.in_(["partially_successful", "successful"]))
        .group_by(FoiRequest.campaign_id)
        .subquery()
    )

    unres = (
        select(Message.foi_request_id, func.max(Message.timestamp))
        .filter(~Message.foi_request_id.in_(resolved_mess))
        .group_by(Message.foi_request_id)
        .subquery()
    )

    late_res = (
        select(FoiRequest.id)
        .join(res_date, FoiRequest.id == res_date.c.foi_request_id)
        .where(FoiRequest.due_date < res_date.c.min)
        .subquery()
    )

    late_unres = (
        select(FoiRequest.id)
        .join(unres, FoiRequest.id == unres.c.foi_request_id)
        .where(FoiRequest.due_date < unres.c.max)
        .subquery()
    )

    late_all = (
        select(func.coalesce(late_res.c.id, late_unres.c.id).label("id"))
        .join(late_unres, late_res.c.id == late_unres.c.id, full=True)
        .subquery()
    )

    late = (
        select(FoiRequest.campaign_id, func.count(late_all.c.id.distinct()))
        .join(late_all, FoiRequest.id == late_all.c.id, isouter=True)
        .group_by(FoiRequest.campaign_id)
        .subquery()
    )

    late = select(late.c.campaign_id, case((late.c.count.isnot(None), late.c.count), else_=0).label("count")).subquery()

    if ascending:
        ordering = asc
    else:
        ordering = desc

    if s in ["Anzahl", "Erfolgsquote", "Verspätungsquote", "Abgeschlossenenquote", "Erfolgreich"]:
        stmt = (
            select(
                Campaign.name,
                total_num.c.count.label("Anzahl"),
                (cast(resolved.c.count, Float) / total_num.c.count * 100).label("Abgeschlossenenquote"),
                late.c.count.label("Fristüberschreitungen"),
                (cast(late.c.count, Float) / total_num.c.count * 100).label("Verspätungsquote"),
                func.sum(successful.c.count).label("Erfolgreich"),
                (cast(successful.c.count, Float) / total_num.c.count * 100).label("Erfolgsquote"),
            )
            .join(resolved, Campaign.id == resolved.c.campaign_id)
            .join(total_num, Campaign.id == total_num.c.campaign_id)
            .join(late, late.c.campaign_id == Campaign.id, isouter=True)
            .join(successful, successful.c.campaign_id == Campaign.id, isouter=True)
            .where(total_num.c.campaign_id == resolved.c.campaign_id)
            .where(total_num.c.count > 20)
            .group_by(
                Campaign.name,
                total_num.c.count,
                resolved.c.count,
                late.c.count,
                successful.c.count,
            )
            .order_by(nullslast(ordering(s)))
            .limit(10)
        )
    else:
        stmt = (
            select(
                Campaign.name,
                total_num.c.count.label("Anzahl"),
                (cast(resolved.c.count, Float) / total_num.c.count * 100).label("Abgeschlossenenquote"),
                late.c.count.label("Fristüberschreitungen"),
                (cast(late.c.count, Float) / total_num.c.count * 100).label("Verspätungsquote"),
                func.sum(successful.c.count).label("Erfolgreich"),
                (cast(successful.c.count, Float) / total_num.c.count * 100).label("Erfolgsquote"),
            )
            .join(resolved, Campaign.id == resolved.c.campaign_id)
            .join(total_num, Campaign.id == total_num.c.campaign_id)
            .join(late, late.c.campaign_id == Campaign.id, isouter=True)
            .join(successful, successful.c.campaign_id == Campaign.id, isouter=True)
            .where(total_num.c.campaign_id == resolved.c.campaign_id)
            .where(total_num.c.count > 20)
            .order_by(nullslast("Verspätungsquote"))
            .limit(10)
        )

    result = db.execute(stmt).fetchall()
    return to_dct(result)


def query_ranking(db, typ, s, ascending):
    if typ == "public_bodies":
        return {"ranking": ranking_public_body(db, s=s, ascending=ascending)}
    elif typ == "jurisdictions":
        return {"ranking": ranking_jurisdictions(db, s=s, ascending=ascending)}
    elif typ == "campaigns":
        return {"ranking": ranking_campaign(db, s=s, ascending=ascending)}
