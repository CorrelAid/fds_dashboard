from sqlalchemy.orm import Session
from sqlalchemy import func
from models import FoiRequest, PublicBody, Jurisdiction, Campaign, Message
from sqlalchemy import select, text, MetaData, Table, asc, desc, cast, DECIMAL, Float, literal, case
from datetime import datetime


def campaign_start_dates(db, typ, s):
    if s == None:
        stmt = select(Campaign.name.distinct(), Campaign.start_date).order_by(asc(Campaign.start_date))

    elif typ == 'public_bodies':
        relevant_campaigns = select(FoiRequest.campaign_id.distinct()).where(FoiRequest.public_body_id == s)
        stmt = select(Campaign.name.distinct(), Campaign.start_date).filter(Campaign.id.in_(relevant_campaigns))\
            .order_by(asc(Campaign.start_date))
        
    elif typ == 'jurisdictions':
        relevant_campaigns = select(FoiRequest.campaign_id.distinct()).where(FoiRequest.jurisdiction_id == s)
        stmt = select(Campaign.name.distinct(), Campaign.start_date).filter(Campaign.id.in_(relevant_campaigns))\
            .order_by(asc(Campaign.start_date))
    elif typ == 'campaigns':
        stmt = select(Campaign.name.distinct(), Campaign.start_date).where(Campaign.id == s)
        
    result = db.execute(stmt).fetchall()
    result = [{"xAxis": row[1], "name": row[0]} for row in result]
    return result


def query_campaign_starts(db, typ, s):
    return {"campaign_starts": campaign_start_dates(db, typ, s)}