from models import PublicBody, Jurisdiction, Campaign
from sqlalchemy import select, asc


def drop_down_options(db, table):
    stmt = select(table.id.distinct(), table.name).order_by(asc(table.name))
    result = db.execute(stmt).fetchall()
    result = [{"id": row[0], "name": row[1]} for row in result]

    return result


def query_general_info(db, s=None, ascending=None):
    return {
        "jurisdictions": drop_down_options(db, Jurisdiction),
        "public_bodies": drop_down_options(db, PublicBody),
        "campaigns": drop_down_options(db, Campaign),
    }
