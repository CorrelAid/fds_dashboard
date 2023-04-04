from sqlalchemy.orm import Session
from sqlalchemy import func
from models import FoiRequest, PublicBody, Jurisdiction, Campaign, Message
from sqlalchemy import select, text, MetaData, Table, asc, desc, cast, DECIMAL, Float, literal, case
from datetime import datetime

def drop_down_options(db, table):
    stmt = select(table.id.distinct(), table.name).order_by(asc(table.name))
    result = db.execute(stmt).fetchall()
    result = [tuple(row) for row in result]
    print(result)
    return result

def campaign_start_dates(db):
    stmt = select(Campaign.id.distinct(), Campaign.start_date).order_by(asc(Campaign.start_date))
    result = db.execute(stmt).fetchall()
    result = [tuple(row) for row in result]
    return result


def query_general_info(db, l = None, s = None, ascending = None):
    return {"jurisdictions": drop_down_options(db, Jurisdiction),
            "public_bodies": drop_down_options(db, PublicBody),
            "campaign_starts": campaign_start_dates(db)}