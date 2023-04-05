from sqlalchemy.orm import Session
from sqlalchemy import func
from models import FoiRequest, PublicBody, Jurisdiction, Campaign, Message
from sqlalchemy import select, text, MetaData, Table, asc, desc, cast, DECIMAL, Float, literal, case
from datetime import datetime

def drop_down_options(db, table):
    stmt = select(table.id.distinct(), table.name).order_by(asc(table.name))
    result = db.execute(stmt).fetchall()
    result = [{"id":row[0], "name":row[1]} for row in result]
    
    return result




def query_general_info(db, l = None, s = None, ascending = None):
    return {"jurisdictions": drop_down_options(db, Jurisdiction),
            "public_bodies": drop_down_options(db, PublicBody)}