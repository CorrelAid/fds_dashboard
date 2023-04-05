from sqlalchemy.orm import Session
from sqlalchemy import func
from models import FoiRequest, PublicBody, Jurisdiction, Campaign, Message
from sqlalchemy import select, text, MetaData, Table, asc, desc, cast, DECIMAL, Float, literal, case
from datetime import datetime


def campaign_start_dates(db):
    stmt = select(Campaign.name.distinct(), Campaign.start_date).order_by(asc(Campaign.start_date))
    result = db.execute(stmt).fetchall()
    result = [{"xAxis": row[1], "name": row[0]} for row in result]
    return result


def query_campaign_starts(db):
    return {"campaign_starts": campaign_start_dates(db)}