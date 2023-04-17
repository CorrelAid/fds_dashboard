from sqlalchemy.orm import Session
from sqlalchemy import func
from models import FoiRequest, PublicBody, Jurisdiction, Campaign, Message
from sqlalchemy import select, text, MetaData, Table, asc, desc, cast, DECIMAL, Float, literal, case
from datetime import datetime
from sqlalchemy.dialects import postgresql


def initial_reaction_time(db, typ, s):
    if s == None and typ == None:
        starter = select(Message.foi_request_id.label('id'), func.min(Message.timestamp))\
                    .where(Message.sender_public_body_id == None)\
                    .where(Message.recipient_public_body_id != None)\
                    .group_by(Message.foi_request_id).subquery()

        reaction = select(Message.foi_request_id.label('id'), func.min(Message.timestamp))\
                    .where(Message.sender_public_body_id != None)\
                    .where(Message.recipient_public_body_id == None)\
                    .group_by(Message.foi_request_id).subquery()

    elif typ == "PublicBody": 
        print('here')  
        starter = select(Message.foi_request_id.label('id'), func.min(Message.timestamp))\
                    .where(Message.sender_public_body_id == None)\
                    .where(Message.recipient_public_body_id == s)\
                    .group_by(Message.foi_request_id).subquery()

        reaction = select(Message.foi_request_id.label('id'), func.min(Message.timestamp))\
                    .where(Message.sender_public_body_id == s)\
                    .where(Message.recipient_public_body_id == None)\
                    .group_by(Message.foi_request_id).subquery()

    elif typ == "Jurisdiction":
        starter = select(Message.foi_request_id.label('id'), func.min(Message.timestamp))\
                    .join(PublicBody, Message.recipient_public_body_id == PublicBody.id)\
                    .where(Message.sender_public_body_id == None)\
                    .where(PublicBody.jurisdiction_id == s)\
                    .group_by(Message.foi_request_id).subquery()

        reaction = select(Message.foi_request_id.label('id'), func.min(Message.timestamp))\
                    .join(PublicBody, Message.sender_public_body_id == PublicBody.id)\
                    .where(PublicBody.jurisdiction_id == s)\
                    .where(Message.recipient_public_body_id == None)\
                    .group_by(Message.foi_request_id).subquery()
        
    elif typ == "Campaign":
        starter = select(Message.foi_request_id.label('id'), func.min(Message.timestamp))\
                    .join(FoiRequest, Message.foi_request_id == FoiRequest.id)\
                    .where(Message.sender_public_body_id == None)\
                    .where(Message.recipient_public_body_id != None)\
                    .where(FoiRequest.campaign_id == s)\
                    .group_by(Message.foi_request_id).subquery()

        reaction = select(Message.foi_request_id.label('id'), func.min(Message.timestamp))\
                    .join(FoiRequest, Message.foi_request_id == FoiRequest.id)\
                    .where(Message.sender_public_body_id != None)\
                    .where(Message.recipient_public_body_id == None)\
                    .where(FoiRequest.campaign_id == s)\
                    .group_by(Message.foi_request_id).subquery()

    combine = select(reaction.c.id, (reaction.c.min - starter.c.min).label('time'))\
                    .select_from(reaction.join(starter, reaction.c.id == starter.c.id)).subquery()

    average = select(func.avg(combine.c.time))

    result = db.execute(average).fetchall()
    result = [tuple(row) for row in result]
    print('start')
    print(result)
    print(result[0][0])
    return result[0][0]


def resolved_time(db, typ, s):
    if s == None and typ == None:
        starter = select(Message.foi_request_id.label('id'), func.min(Message.timestamp))\
                    .where(Message.sender_public_body_id == None)\
                    .where(Message.recipient_public_body_id != None)\
                    .group_by(Message.foi_request_id).subquery()

        reaction = select(Message.foi_request_id.label('id'), func.min(Message.timestamp))\
                    .filter(Message.status.in_(['resolved', 'partially_successful', 'successful']))\
                    .group_by(Message.foi_request_id).subquery()
        
    elif typ == "PublicBody": 
        starter = select(Message.foi_request_id.label('id'), func.min(Message.timestamp))\
                    .where(Message.sender_public_body_id == None)\
                    .where(Message.recipient_public_body_id == s)\
                    .group_by(Message.foi_request_id).subquery()

        reaction = select(Message.foi_request_id.label('id'), func.min(Message.timestamp))\
                    .filter(Message.status.in_(['resolved', 'partially_successful', 'successful']))\
                    .where(Message.sender_public_body_id == s)\
                    .group_by(Message.foi_request_id).subquery()
        
    elif typ == "Jurisdiction":
        starter = select(Message.foi_request_id.label('id'), func.min(Message.timestamp))\
                    .join(PublicBody, Message.recipient_public_body_id == PublicBody.id)\
                    .where(Message.sender_public_body_id == None)\
                    .where(PublicBody.jurisdiction_id == s)\
                    .group_by(Message.foi_request_id).subquery()

        reaction = select(Message.foi_request_id.label('id'), func.min(Message.timestamp))\
                    .join(PublicBody, Message.sender_public_body_id == PublicBody.id)\
                    .filter(Message.status.in_(['resolved', 'partially_successful', 'successful']))\
                    .where(PublicBody.jurisdiction_id == s)\
                    .group_by(Message.foi_request_id).subquery()
        
    elif typ == "Campaign":
        starter = select(Message.foi_request_id.label('id'), func.min(Message.timestamp))\
                    .join(FoiRequest, Message.foi_request_id == FoiRequest.id)\
                    .where(Message.sender_public_body_id == None)\
                    .where(FoiRequest.campaign_id == s)\
                    .group_by(Message.foi_request_id).subquery()

        reaction = select(Message.foi_request_id.label('id'), func.min(Message.timestamp))\
                    .join(FoiRequest, Message.foi_request_id == FoiRequest.id)\
                    .filter(Message.status.in_(['resolved', 'partially_successful', 'successful']))\
                    .where(FoiRequest.campaign_id == s)\
                    .group_by(Message.foi_request_id).subquery()
        
    combine = select(reaction.c.id, (reaction.c.min - starter.c.min).label('time'))\
                    .select_from(reaction.join(starter, reaction.c.id == starter.c.id)).subquery()

    average = select(func.avg(combine.c.time))

    print(average)

    result = db.execute(average).fetchall()
    result = [tuple(row) for row in result]
    print(result)
    print(result[0][0])
    return result[0][0]

def query_reaction_time(db, typ, s,  l = None, ascending = None):
    return {"initial_reaction_time": initial_reaction_time(db, typ, s),
            "resolved_time": resolved_time(db, typ, s)}
            #,
          #  "reaction_time": drop_down_options(db, PublicBody)}


