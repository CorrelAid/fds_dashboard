from api.models import PublicBody, Jurisdiction, Campaign, FoiRequest
from sqlalchemy import select, asc, func


def drop_down_options(db, table, id_col):
    subquery = select(id_col).group_by(id_col).having(func.count() > 0).subquery()
    stmt = select(table.id.distinct(), table.name).where(table.id.in_(subquery)).order_by(asc(table.name))
    print(stmt)
    result = db.execute(stmt).fetchall()
    result = [{"id": row[0], "name": row[1]} for row in result]

    return result


def query_general_info(db, s=None, ascending=None):
    return {
        "jurisdictions": drop_down_options(db, Jurisdiction, FoiRequest.jurisdiction_id),
        "public_bodies": drop_down_options(db, PublicBody, FoiRequest.public_body_id),
        "campaigns": drop_down_options(db, Campaign, FoiRequest.campaign_id),
    }
