from sqlalchemy import func
from api.models import FoiRequest, Message
from sqlalchemy import select, cast, Float, case


def resolved_(db, table, level, selection):
    if level is not None and selection is not None:
        stmt = (
            select(cast(func.count(table.id), Float).label("value"))
            .where(getattr(table, level) == selection)
            .where(FoiRequest.status == "resolved")
            .group_by(FoiRequest.status)
        )
    else:
        stmt = (
            select(cast(func.count(table.id), Float).label("value"))
            .where(FoiRequest.status == "resolved")
            .group_by(FoiRequest.status)
        )
    result = db.execute(stmt).fetchall()
    result = [tuple(row) for row in result]
    print(f"RESULT.{result}")
    if result:
        result = result[0][0]
    else:
        result = 0
    return result


def group_by_count(db, table, column, level, selection):
    if level is not None and selection is not None:
        pre = (
            select(column.label("name"), func.count(table.id).label("value"))
            .where(getattr(table, level) == selection)
            .group_by(column)
            .subquery()
        )
    else:
        pre = select(column.label("name"), func.count(table.id).label("value")).group_by(column).subquery()

    if column == FoiRequest.status:
        stmt = select(pre.c.name, pre.c.value).where(pre.c.name != "resolved")
    else:
        stmt = select(pre.c.name, pre.c.value)

    result = db.execute(stmt).fetchall()

    result = [{"value": row[1], "name": row[0]} for row in result]

    return result


def requests_by_month(db, table, column, level, selection):
    if level is not None and selection is not None:
        stmt = (
            select(func.date_trunc("month", column), func.count(table.id))
            .where(getattr(table, level) == selection)
            .group_by(func.date_trunc("month", column))
            .order_by(func.date_trunc("month", column))
        )
    else:
        stmt = (
            select(func.date_trunc("month", column), func.count(table.id))
            .group_by(func.date_trunc("month", column))
            .order_by(func.date_trunc("month", column))
        )
    result = db.execute(stmt).fetchall()
    lst = []
    value = 0
    for row in result:
        value += row[1]
        obj = {"value": value, "name": row[0]}
        lst.append(obj)
    return lst


def user_count(db, table, level, selection):
    if level is not None and selection is not None:
        stmt = select(func.count(table.user_id.distinct())).where(getattr(table, level) == selection)
    else:
        stmt = select(func.count(table.user_id.distinct()))
    result = db.execute(stmt).fetchall()
    result = [tuple(row) for row in result]
    return result[0][0]


def request_count(db, table, level, selection):
    if level is not None and selection is not None:
        stmt = select(func.count(table.id.distinct())).where(getattr(table, level) == selection)
    else:
        stmt = select(func.count(table.id.distinct()))
    result = db.execute(stmt).fetchall()
    result = [tuple(row) for row in result]
    return result[0][0]


def percentage_costs(db, level, selection):
    if level is None and selection is None:
        not_free = select(FoiRequest.id).where(FoiRequest.costs != 0.0).subquery()
        stmt = select(
            cast(func.count(not_free.c.id.distinct()), Float) / cast(func.count(FoiRequest.id.distinct()), Float) * 100
        ).join(not_free, not_free.c.id == FoiRequest.id, isouter=True)
    else:
        not_free = (
            select(FoiRequest.id)
            .where(FoiRequest.costs != 0.0)
            .where(getattr(FoiRequest, level) == selection)
            .subquery()
        )
        stmt = (
            select(
                case(
                    (
                        cast(func.count(not_free.c.id.distinct()), Float) > 0,
                        (
                            func.count(not_free.c.id.distinct())
                            / (cast(func.count(FoiRequest.id.distinct()), Float))
                            * 100
                        ).label("percentage"),
                    ),
                    else_=cast(0, Float).label("percentage"),
                )
            )
            #  func.count(not_free.c.id.distinct()) / (cast(func.count(FoiRequest.id.distinct()), Float)) * 100)
            .join(not_free, not_free.c.id == FoiRequest.id, isouter=True).where(getattr(FoiRequest, level) == selection)
        )

    result = db.execute(stmt).fetchall()
    result = [tuple(row) for row in result]
    return result[0][0]


def withdrew_costs(db, level, selection):
    if level is None and selection is None:
        not_free = select(FoiRequest.id).where(FoiRequest.costs != 0.0).subquery()
        withdrawn = (
            select(FoiRequest.id)
            .where(FoiRequest.costs != 0.0)
            .where(FoiRequest.resolution == "user_withdrew_costs")
            .subquery()
        )

    else:
        not_free = (
            select(FoiRequest.id)
            .where(FoiRequest.costs != 0.0)
            .where(getattr(FoiRequest, level) == selection)
            .subquery()
        )

        withdrawn = (
            select(FoiRequest.id)
            .where(FoiRequest.costs != 0.0)
            .where(FoiRequest.resolution == "user_withdrew_costs")
            .where(getattr(FoiRequest, level) == selection)
            .subquery()
        )

    stmt = (
        select(
            case(
                (
                    cast(func.count(withdrawn.c.id.distinct()), Float) > 0,
                    (
                        cast(func.count(withdrawn.c.id.distinct()), Float)
                        / (cast(func.count(not_free.c.id.distinct()), Float))
                        * 100
                    ).label("result"),
                ),
                else_=cast(0, Float).label("result"),
            )
        )
        .select_from(not_free)
        .join(withdrawn, not_free.c.id == withdrawn.c.id, isouter=True)
    )

    result = db.execute(stmt).fetchall()
    result = [tuple(row) for row in result]
    return result[0][0]


def min_costs(db, level, selection):
    if level is None and selection is None:
        stmt = select(cast(func.min(FoiRequest.costs), Float)).where(FoiRequest.costs != 0)

    else:
        stmt = (
            select(cast(func.min(FoiRequest.costs), Float))
            .where(FoiRequest.costs != 0)
            .where(getattr(FoiRequest, level) == selection)
        )
    result = db.execute(stmt).fetchall()
    result = [tuple(row) for row in result]
    if result is None:
        result = 0
    else:
        result = result[0][0]
    return result


def max_costs(db, level, selection):
    if level is None and selection is None:
        stmt = select(func.max(FoiRequest.costs)).where(FoiRequest.costs != 0)

    else:
        stmt = (
            select(func.max(FoiRequest.costs))
            .where(FoiRequest.costs != 0)
            .where(getattr(FoiRequest, level) == selection)
        )

    result = db.execute(stmt).fetchall()
    result = [tuple(row) for row in result]
    if result is None:
        result = 0
    else:
        result = result[0][0]
    return result


def avg_costs(db, level, selection):
    if level is None and selection is None:
        stmt = select(func.avg(FoiRequest.costs)).where(FoiRequest.costs != 0)

    else:
        stmt = (
            select(func.avg(FoiRequest.costs))
            .where(FoiRequest.costs != 0)
            .where(getattr(FoiRequest, level) == selection)
        )

    result = db.execute(stmt).fetchall()
    result = [tuple(row) for row in result]
    if result is None:
        result = 0
    else:
        result = result[0][0]
    return result


def overall_rates(db, level, selection):
    resolved_mess = (
        select(Message.foi_request_id.distinct().label("foi_request_id"))
        .filter(Message.status.in_(["resolved", "partially_successful", "successful"]))
        .subquery()
    )

    res_date = (
        select(Message.foi_request_id, func.min(Message.timestamp))
        .filter(Message.foi_request_id.in_(resolved_mess))
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
        .where(FoiRequest.due_date < res_date.c.min)
        .subquery()
    )

    late_unres = (
        select(FoiRequest.id)
        .join(unres, FoiRequest.id == unres.c.foi_request_id)
        .where(FoiRequest.due_date < unres.c.max)
        .subquery()
    )

    late = (
        select(func.coalesce(late_res.c.id, late_unres.c.id).label("id"))
        .join(late_unres, late_res.c.id == late_unres.c.id, full=True)
        .subquery()
    )

    if level is None and selection is None:
        stmt = (
            select(
                func.count(FoiRequest.id.distinct()).label("Anzahl"),
                cast(func.count(resolved_mess.c.foi_request_id), Float).label("Anzahl_Erfolgreich"),
                cast(func.count(late.c.id), Float).label("Fristueberschreitungen"),
            )
            .select_from(FoiRequest)
            .join(late, late.c.id == FoiRequest.id, isouter=True)
            .join(resolved_mess, FoiRequest.id == resolved_mess.c.foi_request_id, isouter=True)
            .subquery()
        )

        final = select(
            stmt.c.Anzahl.label("Anzahl"),
            case(
                cast(stmt.c.Anzahl_Erfolgreich, Float) > 0,
                (cast(stmt.c.Anzahl_Erfolgreich, Float) / stmt.c.Anzahl * 100).label("Erfolgsquote"),
                else_=cast(0, Float).label("Erfolgsquote"),
            ),
            cast(stmt.c.Fristueberschreitungen, Float),
            case(
                cast(stmt.c.Fristueberschreitungen, Float) > 0,
                (cast(stmt.c.Fristueberschreitungen, Float) / stmt.c.Anzahl * 100).label("Verspätungsquote"),
                else_=cast(0, Float).label("Verspätungsquote"),
            ),
        )

    elif level == "public_body_id":
        stmt = (
            select(
                func.count(FoiRequest.id.distinct()).label("Anzahl"),
                cast(func.count(resolved_mess.c.foi_request_id), Float).label("Anzahl_Erfolgreich"),
                cast(func.count(late.c.id), Float).label("Fristueberschreitungen"),
            )
            .join(resolved_mess, FoiRequest.id == resolved_mess.c.foi_request_id, isouter=True)
            .join(late, late.c.id == FoiRequest.id, isouter=True)
            .where(FoiRequest.public_body_id == selection)
        )

        final = select(
            stmt.c.Anzahl.label("Anzahl"),
            (cast(stmt.c.Anzahl_Erfolgreich, Float) / stmt.c.Anzahl * 100).label("Erfolgsquote"),
            stmt.c.Fristueberschreitungen,
            (cast(stmt.c.Fristueberschreitungen, Float) / stmt.c.Anzahl * 100).label("Verspätungsquote"),
        )

    elif level == "jurisdiction_id":
        stmt = (
            select(
                func.count(FoiRequest.id.distinct()).label("Anzahl"),
                cast(func.count(resolved_mess.c.foi_request_id), Float).label("Anzahl_Erfolgreich"),
                cast(func.count(late.c.id), Float).label("Fristueberschreitungen"),
            )
            .join(resolved_mess, FoiRequest.id == resolved_mess.c.foi_request_id, isouter=True)
            .join(late, late.c.id == FoiRequest.id, isouter=True)
            .where(FoiRequest.jurisdiction_id == selection)
        )

        final = select(
            stmt.c.Anzahl.label("Anzahl"),
            (cast(stmt.c.Anzahl_Erfolgreich, Float) / stmt.c.Anzahl * 100).label("Erfolgsquote"),
            stmt.c.Fristueberschreitungen,
            (cast(stmt.c.Fristueberschreitungen, Float) / stmt.c.Anzahl * 100).label("Verspätungsquote"),
        )
    else:
        stmt = (
            select(
                func.count(FoiRequest.id.distinct()).label("Anzahl"),
                cast(func.count(resolved_mess.c.foi_request_id), Float).label("Anzahl_Erfolgreich"),
                cast(func.count(late.c.id), Float).label("Fristueberschreitungen"),
            )
            .join(resolved_mess, FoiRequest.id == resolved_mess.c.foi_request_id, isouter=True)
            .join(late, late.c.id == FoiRequest.id, isouter=True)
            .where(FoiRequest.campaign_id == selection)
        )

        final = select(
            stmt.c.Anzahl.label("Anzahl"),
            (cast(stmt.c.Anzahl_Erfolgreich, Float) / stmt.c.Anzahl * 100).label("Erfolgsquote"),
            stmt.c.Fristueberschreitungen,
            (cast(stmt.c.Fristueberschreitungen, Float) / stmt.c.Anzahl * 100).label("Verspätungsquote"),
        )

    result = db.execute(final).fetchall()
    dct = {}

    dct["number"] = float(result[0][0])
    dct["success_rate"] = float(result[0][1])
    dct["number overdue"] = float(result[0][2])
    dct["overdue_rate"] = float(result[0][3])
    return dct


def query_stats(db, level, selection, ascending=None):
    foi_requests = request_count(db, FoiRequest, level=level, selection=selection)
    resolved = resolved_(db, FoiRequest, level=level, selection=selection)

    return {
        "foi_requests": foi_requests,
        "foi_requests_resolved": resolved,
        "foi_requests_not_resolved": foi_requests - resolved,
        "users": user_count(db, FoiRequest, level=level, selection=selection),
        "dist_resolution": group_by_count(db, FoiRequest, FoiRequest.resolution, level=level, selection=selection),
        "dist_status": group_by_count(db, FoiRequest, FoiRequest.status, level=level, selection=selection),
        "requests_by_month": requests_by_month(db, FoiRequest, FoiRequest.created_at, level=level, selection=selection),
        "percentage_costs": percentage_costs(db, level=level, selection=selection),
        "percentage_withdrawn": withdrew_costs(db, level, selection),
        "min_costs": min_costs(db, level, selection),
        "max_costs": max_costs(db, level, selection),
        "avg_costs": avg_costs(db, level, selection),
        "success_rate": overall_rates(db, level=level, selection=selection),
    }
