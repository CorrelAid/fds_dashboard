from sqlalchemy import func
from api.models import FoiRequest, PublicBody, Jurisdiction, Campaign, Message
from sqlalchemy import select, asc, desc, cast, Float, case, or_, nullslast


def ranking(db, s: str, ascending: bool, category: str):
    total_num = (
        select(FoiRequest.public_body_id, func.count(FoiRequest.id.distinct()))
        .where(FoiRequest.public_body_id is not None)
        # .filter(or_(FoiRequest.campaign_id != 9, FoiRequest.campaign_id is None))
        .group_by(FoiRequest.public_body_id)
        .subquery()
    )
    if category == "campaigns":
        total_num = (
            select(FoiRequest.campaign_id, func.count(FoiRequest.id.distinct()))
            .group_by(FoiRequest.campaign_id)
            .subquery()
        )

    resolved_mess = (
        select(Message.foi_request_id.distinct())
        .filter(
            Message.status.in_(
                [
                    "resolved",
                ]
            )
        )
        .subquery()
    )

    res_date = (
        select(Message.foi_request_id, func.min(Message.timestamp))
        .filter(Message.foi_request_id.in_(resolved_mess))
        .group_by(Message.foi_request_id)
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
    if category == "campaigns":
        resolved = (
            select(FoiRequest.campaign_id, func.count(FoiRequest.id.distinct()))
            .filter(FoiRequest.id.in_(resolved_mess))
            .group_by(FoiRequest.campaign_id)
            .subquery()
        )

    successful = (
        select(FoiRequest.public_body_id, func.count(FoiRequest.id.distinct()))
        .where(FoiRequest.public_body_id is not None)
        # .filter(or_(FoiRequest.campaign_id != 9, FoiRequest.campaign_id is None))
        .filter(FoiRequest.resolution.in_(["partially_successful", "successful"]))
        .group_by(FoiRequest.public_body_id)
        .subquery()
    )
    if category == "campaigns":
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
        # .filter(or_(FoiRequest.campaign_id != 9, FoiRequest.campaign_id is None))
        .where(FoiRequest.due_date < res_date.c.min)
        .subquery()
    )

    late_unres = (
        select(FoiRequest.id)
        .join(unres, FoiRequest.id == unres.c.foi_request_id)
        # .filter(or_(FoiRequest.campaign_id != 9, FoiRequest.campaign_id is None))
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
    if category == "campaigns":
        late = select(
            late.c.campaign_id, case((late.c.count.isnot(None), late.c.count), else_=0).label("count")
        ).subquery()

    if ascending:
        ordering = asc
    else:
        ordering = desc

    stmt = select(
        PublicBody.name,
        total_num.c.count.label("Anzahl"),
        (cast(resolved.c.count, Float) / total_num.c.count * 100).label("Abgeschlossenenquote"),
        late.c.count.label("Fristüberschreitungen"),
        (cast(late.c.count, Float) / total_num.c.count * 100).label("Verspätungsquote"),
        cast(successful.c.count, Float).label("Erfolgreich"),
        (cast(successful.c.count, Float) / total_num.c.count * 100).label("Erfolgsquote"),
    )

    if category == "public_bodies":
        stmt = (
            stmt.join(resolved, PublicBody.id == resolved.c.public_body_id)
            .join(total_num, PublicBody.id == total_num.c.public_body_id)
            .join(late, late.c.public_body_id == PublicBody.id, isouter=True)
            .join(successful, PublicBody.id == successful.c.public_body_id, isouter=True)
            .where(total_num.c.public_body_id == resolved.c.public_body_id)
            .where(total_num.c.count > 20)
        )

    elif category == "jurisdictions":
        stmt = (
            stmt.join(PublicBody, Jurisdiction.id == PublicBody.jurisdiction_id)
            .join(resolved, PublicBody.id == resolved.c.public_body_id)
            .join(total_num, PublicBody.id == total_num.c.public_body_id)
            .join(late, late.c.public_body_id == PublicBody.id, isouter=True)
            .join(successful, PublicBody.id == successful.c.public_body_id, isouter=True)
            .where(total_num.c.public_body_id == resolved.c.public_body_id)
            .group_by(Jurisdiction.name)
        )

    elif category == "campaigns":
        stmt = (
            stmt.join(resolved, Campaign.id == resolved.c.campaign_id)
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
        )
    if s in ["Anzahl", "Erfolgsquote", "Verspätungsquote", "Abgeschlossenenquote", "Erfolgreich"]:
        stmt = stmt.order_by(nullslast(ordering(s))).limit(10)
    else:
        stmt = stmt.order_by(nullslast(ordering("Anzahl"))).limit(10)

    result = db.execute(stmt).fetchall()

    result = db.execute(stmt).fetchall()

    lst = []
    for row in result:
        dct = {
            "name": str(row[0]),
            "number": int(row[1]),
            "resolution_rate": float(row[2]),
            "number_overdue": int(row[3]),
            "overdue_rate": float(row[4]),
            "successful": float(row[5]) if row[5] is not None else 0,
            "success_rate": float(row[6]) if row[6] is not None else 0,
        }
        lst.append(dct)

    return lst


def query_ranking(db, category, s, ascending):
    return {"ranking": ranking(db, s=s, ascending=ascending, category=category)}
