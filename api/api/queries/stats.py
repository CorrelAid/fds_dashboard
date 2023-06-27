from api.models import FoiRequest, Message, PublicBody
from sqlalchemy import select, cast, Float, desc, func


def request_count(db, table, category=None, selection=None):
    stmt = select(func.count(table.id.distinct()))

    if category is not None and selection is not None:
        stmt = stmt.where(getattr(table, category) == selection)

    result = db.execute(stmt).fetchone()
    count = result[0] if result else 0
    return count


def group_by_count(db, table, column, category=None, selection=None):
    stmt = select(column.label("name"), func.count(table.id).label("value"))

    if category is not None and selection is not None:
        stmt = stmt.where(getattr(table, category) == selection)

    if column == FoiRequest.resolution:
        stmt = stmt.where(FoiRequest.status == "resolved")

    stmt = stmt.group_by(column)

    result = db.execute(stmt).fetchall()

    result = [{"value": row[1], "name": row[0]} for row in result]

    result = sorted(result, key=lambda x: x["value"], reverse=True)

    return result


def fractional_days(delta):
    return round(delta.total_seconds() / (24 * 60 * 60), 2)


def gen_perc(value, total):
    return value / total * 100 if total > 0 else 0.0


def translate(x):
    translations = {
        # Resolution
        "user_withdrew": "Zurückgezogen",
        "not_held": "Information nicht vorhanden",
        "partially_successful": "Teilweise erfolgreich",
        "successful": "Erfolgreich",
        "refused": "Abgelehnt",
        "user_withdrew_costs": "Wegen Kosten zurückgezogen",
        "resolved": "Abgeschlossen",
        "": "Unbekannt",  # Empty string key remains the same
        # Status
        "awaiting_response": "Wartet auf Antwort",
        "overdue": "Antwort überfällig",
        "asleep": "Eingeschlafen",
        "awaiting_user_confirmation": "Wartet auf Nutzerbestätigung",
        "publicbody_needed": "Behörde erforderlich",
    }
    return translations[x]


def proc_dist_resolution(dist_resolution):
    # summing up withdrawal reasons and add to user_withdrew
    withdrawn_sum = sum(
        entry["value"] for entry in dist_resolution if entry["name"] in ["user_withdrew", "user_withdrew_costs"]
    )
    for entry in dist_resolution:
        if entry["name"] == "user_withdrew":
            entry["value"] = withdrawn_sum
    # translate name and filter our user_withdrew_costs
    dist_resolution = [
        {"name": translate(d["name"]), "value": d["value"]}
        for d in dist_resolution
        if d["name"] != "user_withdrew_costs"
    ]
    return dist_resolution


def proc_dist_status(dist_status):
    # removing status == resolved
    dist_status = [
        {"name": translate(d["name"]), "value": d["value"]}
        for d in dist_status
        if d["name"] != "resolved" and d["name"] != "asleep"
    ]

    return dist_status


def proc_value_status(dist_status, key):
    try:
        return [d for d in dist_status if d["name"] == key][0]["value"]
    except IndexError:
        return 0


def proc_asleep_percentage(asleep, foi_requests):
    return gen_perc(asleep, foi_requests)


def proc_overdue_rate(overdue, foi_requests):
    return gen_perc(overdue, foi_requests)


def requests_by_month(db, table, column, category=None, selection=None):
    stmt = (
        select(func.date_trunc("month", column), func.count(table.id))
        .group_by(func.date_trunc("month", column))
        .order_by(func.date_trunc("month", column))
    )

    if category is not None and selection is not None:
        stmt = stmt.where(getattr(table, category) == selection)

    result = db.execute(stmt).fetchall()
    lst = []
    value = 0
    for row in result:
        value += row[1]
        obj = {"value": value, "name": row[0]}
        lst.append(obj)
    return lst


def user_count(db, table, category=None, selection=None):
    stmt = select(func.count(table.user_id.distinct()))

    if category is not None and selection is not None:
        stmt = stmt.where(getattr(table, category) == selection)

    result = db.execute(stmt).scalar()
    return result


def percentage_costs(db, category, selection):
    not_free = select(FoiRequest.id).where(FoiRequest.costs != 0.0)

    if category is not None and selection is not None:
        not_free = not_free.where(getattr(FoiRequest, category) == selection)
        total_count = db.scalar(
            select(func.count(FoiRequest.id.distinct())).where(getattr(FoiRequest, category) == selection)
        )
    else:
        total_count = db.scalar(select(func.count(FoiRequest.id.distinct())))
    not_free_count = db.scalar(select(func.count(not_free.subquery().c.id.distinct())))

    if total_count == 0:
        percentage = 0
    else:
        percentage = (not_free_count / total_count) * 100

    return percentage


def withdrew_costs(db, category, selection):
    not_free_stmt = select(func.count(FoiRequest.id)).where(FoiRequest.costs != 0.0)
    withdrawn_stmt = (
        select(func.count(FoiRequest.id))
        .where(FoiRequest.costs != 0.0)
        .where(FoiRequest.resolution == "user_withdrew_costs")
    )

    if category is not None and selection is not None:
        not_free_stmt = not_free_stmt.where(getattr(FoiRequest, category) == selection)
        withdrawn_stmt = withdrawn_stmt.where(getattr(FoiRequest, category) == selection)

    not_free_count = db.execute(not_free_stmt).scalar()
    withdrawn_count = db.execute(withdrawn_stmt).scalar()

    if not_free_count == 0:
        result = 0
    else:
        result = (withdrawn_count / not_free_count) * 100

    return result


def costs(db, category, selection):
    max = max_costs(db, category, selection, min=False)
    min = max_costs(db, category, selection, min=True)
    avg = avg_costs(db, category, selection)
    med = med_costs(db, category, selection)

    result = [{"Average": avg, "Median": med, "Min": min, "Max": max}]
    return result


def max_costs(db, category, selection, min: bool):
    stmt = select(FoiRequest.id, cast(FoiRequest.costs, Float)).where(FoiRequest.costs != 0)

    if category is not None and selection is not None:
        stmt = stmt.where(getattr(FoiRequest, category) == selection)

    if not min:
        stmt = stmt.order_by(desc(FoiRequest.costs)).limit(1)
    else:
        stmt = stmt.order_by(FoiRequest.costs).limit(1)
    result = db.execute(stmt).fetchone()
    if result is None:
        result = {"value": 0, "id": None}
    else:
        result = {"value": result[1], "id": result[0]}

    return result


def avg_costs(db, category, selection):
    stmt = select(func.avg(FoiRequest.costs)).where(FoiRequest.costs != 0)
    if category is not None and selection is not None:
        stmt = stmt.where(getattr(FoiRequest, category) == selection)

    result = db.execute(stmt).scalar()

    if result is None:
        result = 0
    return result


def med_costs(db, category, selection):
    stmt = select(func.percentile_cont(0.5).within_group(FoiRequest.costs)).where(FoiRequest.costs != 0)
    if category is not None and selection is not None:
        stmt = stmt.where(getattr(FoiRequest, category) == selection)

    result = db.execute(stmt).scalar()
    if result is None:
        result = 0
    return result


def overdue_requests(db, category, selection):
    resolved_mess = (
        select(Message.foi_request_id.distinct().label("foi_request_id"))
        .filter(Message.status.in_(["resolved"]))
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

    stmt = (
        select(
            func.count(late.c.id).label("Fristueberschreitungen"),
        )
        .select_from(FoiRequest)
        .join(late, late.c.id == FoiRequest.id, isouter=True)
        .join(resolved_mess, FoiRequest.id == resolved_mess.c.foi_request_id, isouter=True)
    )

    if category is not None and selection is not None:
        stmt = stmt.where(getattr(FoiRequest, category) == selection)

    result = db.execute(stmt).fetchone()

    return float(result[0])


def initial_reaction_time(db, category, selection):
    if selection is None and category is None:
        starter = (
            select(Message.foi_request_id.label("id"), func.min(Message.timestamp))
            .where(Message.sender_public_body_id.is_(None))
            .where(Message.recipient_public_body_id.isnot(None))
            .group_by(Message.foi_request_id)
            .subquery()
        )

        reaction = (
            select(Message.foi_request_id.label("id"), func.min(Message.timestamp))
            .join(FoiRequest, Message.foi_request_id == FoiRequest.id)
            .where(Message.timestamp > FoiRequest.created_at)
            .where(Message.sender_public_body_id.isnot(None))
            .where(Message.recipient_public_body_id.is_(None))
            .group_by(Message.foi_request_id)
            .subquery()
        )

    elif category == "public_body_id":
        starter = (
            select(Message.foi_request_id.label("id"), func.min(Message.timestamp))
            .where(Message.sender_public_body_id.is_(None))
            .where(Message.recipient_public_body_id == selection)
            .group_by(Message.foi_request_id)
            .subquery()
        )

        reaction = (
            select(Message.foi_request_id.label("id"), func.min(Message.timestamp))
            .join(FoiRequest, Message.foi_request_id == FoiRequest.id)
            .where(Message.timestamp > FoiRequest.created_at)
            .where(Message.sender_public_body_id == selection)
            .where(Message.recipient_public_body_id.is_(None))
            .group_by(Message.foi_request_id)
            .subquery()
        )

    elif category == "jurisdiction_id":
        starter = (
            select(Message.foi_request_id.label("id"), func.min(Message.timestamp))
            .join(PublicBody, Message.recipient_public_body_id == PublicBody.id)
            .where(Message.sender_public_body_id.is_(None))
            .where(PublicBody.jurisdiction_id == selection)
            .group_by(Message.foi_request_id)
            .subquery()
        )

        reaction = (
            select(Message.foi_request_id.label("id"), func.min(Message.timestamp))
            .join(PublicBody, Message.sender_public_body_id == PublicBody.id)
            .join(FoiRequest, Message.foi_request_id == FoiRequest.id)
            .where(Message.timestamp > FoiRequest.created_at)
            .where(PublicBody.jurisdiction_id == selection)
            .where(Message.recipient_public_body_id.is_(None))
            .group_by(Message.foi_request_id)
            .subquery()
        )

    elif category == "campaign_id":
        starter = (
            select(Message.foi_request_id.label("id"), func.min(Message.timestamp))
            .join(FoiRequest, Message.foi_request_id == FoiRequest.id)
            .where(Message.sender_public_body_id.is_(None))
            .where(Message.recipient_public_body_id.isnot(None))
            .where(FoiRequest.campaign_id == selection)
            .group_by(Message.foi_request_id)
            .subquery()
        )

        reaction = (
            select(Message.foi_request_id.label("id"), func.min(Message.timestamp))
            .join(FoiRequest, Message.foi_request_id == FoiRequest.id)
            .join(FoiRequest, Message.foi_request_id == FoiRequest.id)
            .where(Message.timestamp > FoiRequest.created_at)
            .where(Message.sender_public_body_id.isnot(None))
            .where(Message.recipient_public_body_id.is_(None))
            .where(FoiRequest.campaign_id == selection)
            .group_by(Message.foi_request_id)
            .subquery()
        )

    combine = (
        select(reaction.c.id, (reaction.c.min - starter.c.min).label("time"))
        .select_from(reaction.join(starter, reaction.c.id == starter.c.id))
        .subquery()
    )
    avg = time_function(db, combine, "avg")
    median = time_function(db, combine, "median")
    min = time_function(db, combine, "min")
    max = time_function(db, combine, "max")
    result = [
        {
            "Average": avg,
            "Median": median,
            "Min": {"value": min[1], "id": min[0]},
            "Max": {"value": max[1], "id": max[0]},
        }
    ]
    return result


def time_function(db, input, function):
    if function == "avg":
        stmt = select(func.avg(getattr(input.c, "time")).label("Avg"))

        result = db.execute(stmt).fetchone()
        print(f"AVERAGE: {result}")
        if result[0] is None:
            result = None
        else:
            result = fractional_days(result[0])
        return result

    elif function == "median":
        query = select(func.percentile_cont(0.5).within_group(input.c.time))

        result = db.execute(query).fetchone()
        if result[0] is None:
            result = None
        else:
            result = fractional_days(result[0])
        return result

    elif function == "max":
        stmt = (
            select(getattr(input.c, "id"), getattr(input.c, "time")).order_by(desc(getattr(input.c, "time"))).limit(1)
        )
    elif function == "min":
        stmt = (
            select(getattr(input.c, "id"), getattr(input.c, "time"))
            .where(func.extract("epoch", getattr(input.c, "time")) > 240)
            # at least 5 minutes between first message and answer to filter manually added messages with (almost)
            # same timestamp
            .order_by(getattr(input.c, "time"))
            .limit(1)
        )

    result = db.execute(stmt).fetchone()
    if result is None:
        result1 = []
        result1.append(None)
        result1.append(None)
    else:
        result1 = []
        result1.append(result[0])
        result1.append(fractional_days(result[1]))

    return result1


def resolved_time_prep(db, category, selection):
    if selection is None and category is None:
        starter = (
            select(Message.foi_request_id.label("id"), func.min(Message.timestamp))
            .where(Message.sender_public_body_id.is_(None))
            .where(Message.recipient_public_body_id.isnot(None))
            .group_by(Message.foi_request_id)
            .subquery()
        )

        reaction = (
            select(Message.foi_request_id.label("id"), func.min(Message.timestamp))
            .join(FoiRequest, Message.foi_request_id == FoiRequest.id)
            .where(Message.timestamp > FoiRequest.created_at)
            .filter(Message.status.in_(["resolved", "partially_successful", "successful"]))
            .group_by(Message.foi_request_id)
            .subquery()
        )

    elif category == "public_body_id":
        starter = (
            select(Message.foi_request_id.label("id"), func.min(Message.timestamp))
            .where(Message.sender_public_body_id.is_(None))
            .where(Message.recipient_public_body_id == selection)
            .group_by(Message.foi_request_id)
            .subquery()
        )

        reaction = (
            select(Message.foi_request_id.label("id"), func.min(Message.timestamp))
            .join(FoiRequest, Message.foi_request_id == FoiRequest.id)
            .where(Message.timestamp > FoiRequest.created_at)
            .filter(Message.status.in_(["resolved", "partially_successful", "successful"]))
            .where(Message.sender_public_body_id == selection)
            .group_by(Message.foi_request_id)
            .subquery()
        )

    elif category == "jurisdiction_id":
        starter = (
            select(Message.foi_request_id.label("id"), func.min(Message.timestamp))
            .join(PublicBody, Message.recipient_public_body_id == PublicBody.id)
            .where(Message.sender_public_body_id.is_(None))
            .where(PublicBody.jurisdiction_id == selection)
            .group_by(Message.foi_request_id)
            .subquery()
        )

        reaction = (
            select(Message.foi_request_id.label("id"), func.min(Message.timestamp))
            .join(PublicBody, Message.sender_public_body_id == PublicBody.id)
            .join(FoiRequest, Message.foi_request_id == FoiRequest.id)
            .where(Message.timestamp > FoiRequest.created_at)
            .filter(Message.status.in_(["resolved", "partially_successful", "successful"]))
            .where(PublicBody.jurisdiction_id == selection)
            .group_by(Message.foi_request_id)
            .subquery()
        )

    elif category == "campaign_id":
        starter = (
            select(Message.foi_request_id.label("id"), func.min(Message.timestamp))
            .join(FoiRequest, Message.foi_request_id == FoiRequest.id)
            .where(Message.sender_public_body_id.is_(None))
            .where(FoiRequest.campaign_id == selection)
            .group_by(Message.foi_request_id)
            .subquery()
        )

        reaction = (
            select(Message.foi_request_id.label("id"), func.min(Message.timestamp))
            .join(FoiRequest, Message.foi_request_id == FoiRequest.id)
            .join(FoiRequest, Message.foi_request_id == FoiRequest.id)
            .where(Message.timestamp > FoiRequest.created_at)
            .filter(Message.status.in_(["resolved", "partially_successful", "successful"]))
            .where(FoiRequest.campaign_id == selection)
            .group_by(Message.foi_request_id)
            .subquery()
        )

    combine = (
        select(reaction.c.id, (reaction.c.min - starter.c.min).label("time"))
        .select_from(reaction.join(starter, reaction.c.id == starter.c.id))
        .subquery()
    )
    return combine


def resolved_time(db, category, selection):
    combine = resolved_time_prep(db, category, selection)
    avg = time_function(db, combine, "avg")
    median = time_function(db, combine, "median")
    min = time_function(db, combine, "min")
    max = time_function(db, combine, "max")
    result = [
        {
            "Average": avg,
            "Median": median,
            "Min": {"id": min[0], "value": min[1]},
            "Max": {"id": max[0], "value": max[1]},
        }
    ]
    return result


def refusal_reasons(db, category, selection):
    stmt = (
        select(FoiRequest.refusal_reason, func.count().label("num"))
        .where(
            (FoiRequest.refusal_reason.isnot(None))
            & (FoiRequest.refusal_reason != "")
            & (FoiRequest.refusal_reason != "Gesetz nicht anwendbar")
        )
        .group_by(FoiRequest.refusal_reason)
        .order_by(func.count().desc())
    )
    if category is not None and selection is not None:
        stmt = stmt.where(getattr(FoiRequest, category) == selection)

    stmt = stmt.limit(10)

    result = db.execute(stmt).fetchall()
    refusal_reasons_list = [{"count": row.num, "reason": row.refusal_reason} for row in result]
    return refusal_reasons_list


def refusal_reason_request_count(db, category, selection, conditions):
    stmt = select(func.count()).where(conditions)

    if category is not None and selection is not None:
        stmt = stmt.where(getattr(FoiRequest, category) == selection)

    result = db.execute(stmt).scalar()
    return result


def query_stats(db, category, selection, ascending=None):
    foi_requests = request_count(db, FoiRequest, category=category, selection=selection)
    dist_status = group_by_count(db, FoiRequest, FoiRequest.status, category=category, selection=selection)
    resolved = proc_value_status(dist_status, "resolved")
    not_resolved = foi_requests - resolved
    overdue_total = overdue_requests(db, category=category, selection=selection)
    asleep = proc_value_status(dist_status, "asleep")
    overdue_not_resolved = proc_value_status(dist_status, "overdue")
    refused = refusal_reason_request_count(db, category, selection, (FoiRequest.resolution == "refused"))
    other_or_no_reason = refusal_reason_request_count(
        db, category, selection, (((FoiRequest.refusal_reason == "") & (FoiRequest.resolution == "refused")))
    )
    return {
        "foi_requests": foi_requests,
        "foi_requests_resolved": resolved,
        "foi_requests_not_resolved": not_resolved,
        "users": user_count(db, FoiRequest, category=category, selection=selection),
        "asleep_number": asleep,
        "asleep_percentage_total": proc_asleep_percentage(asleep, foi_requests),
        "asleep_percentage_not_resolved": proc_asleep_percentage(asleep, not_resolved),
        "overdue_not_resolved": overdue_not_resolved,
        "overdue_percentage_not_resolved": gen_perc(overdue_not_resolved, not_resolved),
        "dist_resolution": proc_dist_resolution(
            group_by_count(db, FoiRequest, FoiRequest.resolution, category=category, selection=selection)
        ),
        "dist_status": proc_dist_status(dist_status),
        "overdue_total": overdue_total,
        "overdue_rate": proc_overdue_rate(overdue_total, foi_requests),
        "requests_by_month": requests_by_month(
            db, FoiRequest, FoiRequest.created_at, category=category, selection=selection
        ),
        "initial_reaction_time": initial_reaction_time(db, category=category, selection=selection),
        "resolved_time": resolved_time(db, category=category, selection=selection),
        "percentage_costs": percentage_costs(db, category=category, selection=selection),
        "percentage_withdrawn": withdrew_costs(db, category, selection),
        "costs": costs(db, category, selection),
        "refusal_reasons_specified": gen_perc(
            refusal_reason_request_count(
                db,
                category,
                selection,
                (FoiRequest.refusal_reason.isnot(None))
                & (FoiRequest.refusal_reason != "")
                & (FoiRequest.resolution == "refused")
                & (FoiRequest.refusal_reason != "Gesetz nicht anwendbar"),
            ),
            refused,
        ),
        "no_law_applicable": gen_perc(
            refusal_reason_request_count(
                db,
                category,
                selection,
                (
                    (FoiRequest.refusal_reason.is_(None) | (FoiRequest.refusal_reason == "Gesetz nicht anwendbar"))
                    & (FoiRequest.resolution == "refused")
                ),
            ),
            refused,
        ),
        "other_or_no_reason": gen_perc(other_or_no_reason, refused),
        "refusal_reasons": refusal_reasons(db, category, selection),
    }
