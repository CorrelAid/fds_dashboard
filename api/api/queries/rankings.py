from sqlalchemy.orm import Session
from sqlalchemy import func
from models import FoiRequest, PublicBody, Jurisdiction, Campaign, Message
from sqlalchemy import select, text, MetaData, Table, asc, desc, cast, DECIMAL, Float, literal, case
from datetime import datetime
from sqlalchemy.dialects import postgresql

def ranking(db):
    total_num = select(FoiRequest.public_body_id, func.count(FoiRequest.id.distinct()))\
                        .where(FoiRequest.public_body_id != None)\
                        .group_by(FoiRequest.public_body_id).subquery()

    resolved_mess = select(Message.foi_request_id.distinct())\
                           .where(Message.status == 'resolved').subquery()

    resolved = select(FoiRequest.public_body_id, func.count(FoiRequest.id.distinct()))\
                      .where(FoiRequest.public_body_id != None)\
                      .filter(FoiRequest.id.in_(resolved_mess))\
                      .group_by(FoiRequest.public_body_id).subquery()

    res_date = select(Message.foi_request_id, func.min(Message.timestamp))\
                      .where(Message.status == 'resolved')\
                      .group_by(Message.foi_request_id).subquery()

    unres = select(Message.foi_request_id, func.max(Message.timestamp))\
                   .filter(~Message.foi_request_id.in_(resolved_mess))\
                   .group_by(Message.foi_request_id).subquery()
    
    late_res = select(FoiRequest.id)\
                      .join(res_date, FoiRequest.id == res_date.c.foi_request_id)\
                      .where(FoiRequest.due_date < res_date.c.min).subquery()

    late_unres = select(FoiRequest.id)\
                      .join(unres, FoiRequest.id == unres.c.foi_request_id)\
                      .where(FoiRequest.due_date < unres.c.max).subquery()
    
    late_all = select(func.coalesce(late_res.c.id, late_unres.c.id).label('id'))\
               .join(late_unres, late_res.c.id == late_unres.c.id, full=True).subquery()

    late = select(FoiRequest.public_body_id, func.count(late_all.c.id.distinct()))\
           .join(late_all, FoiRequest.id == late_all.c.id, isouter=True)\
           .group_by(FoiRequest.public_body_id).subquery()   
    
    late2 = select(late.c.public_body_id, case([(late.c.count.isnot(None), late.c.count)], else_=0).label('count')).subquery()

    return late2, total_num, resolved

def ranking_public_body(db, s: str, ascending: bool):
    if ascending:
         ordering = asc
    else:
         ordering = desc
    late, total_num, resolved = ranking(db)
    if s in ['Anzahl', 'Erfolgsquote', 'Verspaetungsquote']:
         stmt = select(PublicBody.name, total_num.c.count.label('Anzahl'), (cast(resolved.c.count, Float)/total_num.c.count * 100).label('Erfolgsquote'), late.c.count.label('Fristüberschreitungen'), (cast(late.c.count, Float)/total_num.c.count * 100).label('Verspaetungsquote'))\
                  .join(resolved, PublicBody.id == resolved.c.public_body_id)\
                  .join(total_num, PublicBody.id == total_num.c.public_body_id)\
                  .join(late, late.c.public_body_id == PublicBody.id)\
                  .where(total_num.c.public_body_id == resolved.c.public_body_id)\
                  .where(total_num.c.count>20)\
                  .order_by(ordering(s))\
                  .limit(10)   
    else:
         stmt = select(PublicBody.name, total_num.c.count.label('Anzahl'), (cast(resolved.c.count, Float)/total_num.c.count * 100).label('Erfolgsquote'), late.c.count.label('Fristüberschreitungen'), (cast(late.c.count, Float)/total_num.c.count * 100).label('Verspaetungsquote'))\
                  .join(resolved, PublicBody.id == resolved.c.public_body_id)\
                  .join(total_num, PublicBody.id == total_num.c.public_body_id)\
                  .join(late, late.c.public_body_id == PublicBody.id)\
                  .where(total_num.c.public_body_id == resolved.c.public_body_id)\
                  .where(total_num.c.count>20)\
                  .order_by('Verspaetungsquote')\
                  .limit(10)          
    print(stmt)                                         
    result = db.execute(stmt).fetchall()
    lst = []
    keys = list(dict(result[0]).keys())
    for row in result:
                dct = {}
                dct["name"] = str(row[keys[0]])
                dct["number"] = int(row[keys[1]])
                dct["success_rate"] = float(row[keys[2]])
                dct["number_overdue"] = int(row[keys[3]])
                dct["overdue_rate"] = float(row[keys[4]])
                lst.append(dct)   
    
    return lst

def ranking_jurisdictions(db, s: str, ascending: bool):
    if ascending:
         ordering = asc
    else:
         ordering = desc 

    late, total_num, resolved = ranking(db)
    if s in ['Anzahl', 'Erfolgsquote', 'Verspaetungsquote']:
         stmt = select(Jurisdiction.name, func.sum(total_num.c.count).label('Anzahl'), (cast(func.sum(resolved.c.count), Float)/func.sum(total_num.c.count) * 100).label('Erfolgsquote'), func.sum(late.c.count).label('Fristüberschreitungen'), (cast(func.sum(late.c.count), Float)/func.sum(total_num.c.count) * 100).label('Verspaetungsquote'))\
                  .join(PublicBody, Jurisdiction.id == PublicBody.jurisdiction_id)\
                  .join(resolved, PublicBody.id == resolved.c.public_body_id)\
                  .join(total_num, PublicBody.id == total_num.c.public_body_id)\
                  .join(late, late.c.public_body_id == PublicBody.id, isouter=True)\
                  .where(total_num.c.public_body_id == resolved.c.public_body_id)\
                  .where(total_num.c.count>50)\
                  .group_by(Jurisdiction.name)\
                  .order_by(ordering(s))\
                  .limit(10)   
    else:
         stmt = select(Jurisdiction.name, func.sum(total_num.c.count).label('Anzahl'), (cast(func.sum(resolved.c.count), Float)/func.sum(total_num.c.count) * 100).label('Erfolgsquote'), func.sum(late.c.count).label('Fristüberschreitungen'), (cast(func.sum(late.c.count), Float)/func.sum(total_num.c.count) * 100).label('Verspaetungsquote'))\
                  .join(PublicBody, Jurisdiction.id == PublicBody.jurisdiction)\
                  .join(resolved, PublicBody.id == resolved.c.public_body_id)\
                  .join(total_num, PublicBody.id == total_num.c.public_body_id)\
                  .join(late, late.c.public_body_id == PublicBody.id, isouter=True)\
                  .where(total_num.c.public_body_id == resolved.c.public_body_id)\
                  .where(total_num.c.count>50)\
                  .group_by(Jurisdiction.name)\
                  .order_by(s)\
                  .limit(10)                                             
    result = db.execute(stmt).fetchall()
    lst = []
    keys = list(dict(result[0]).keys())
    for row in result:
                dct = {}
                dct["name"] = str(row[keys[0]])
                dct["number"] = int(row[keys[1]])
                dct["success_rate"] = float(row[keys[2]])
                dct["number_overdue"] = int(row[keys[3]])
                dct["overdue_rate"] = float(row[keys[4]])
                lst.append(dct)    
    return lst

def ranking_campaign(db, s: str, ascending: bool):
      #                       .where(FoiRequest.public_body_id != 10)\
     total_num = select(FoiRequest.campaign_id, func.count(FoiRequest.id.distinct()))\
                        .group_by(FoiRequest.campaign_id).subquery()

     resolved_mess = select(Message.foi_request_id.distinct())\
                           .where(Message.status == 'resolved').subquery()

     resolved = select(FoiRequest.campaign_id, func.count(FoiRequest.id.distinct()))\
                      .filter(FoiRequest.id.in_(resolved_mess))\
                      .group_by(FoiRequest.campaign_id).subquery()

     res_date = select(Message.foi_request_id, func.min(Message.timestamp))\
                      .where(Message.status == 'resolved')\
                      .group_by(Message.foi_request_id).subquery()

     unres = select(Message.foi_request_id, func.max(Message.timestamp))\
                   .filter(~Message.foi_request_id.in_(resolved_mess))\
                   .group_by(Message.foi_request_id).subquery()
    
     late_res = select(FoiRequest.id)\
                      .join(res_date, FoiRequest.id == res_date.c.foi_request_id)\
                      .where(FoiRequest.due_date < res_date.c.min).subquery()

     late_unres = select(FoiRequest.id)\
                      .join(unres, FoiRequest.id == unres.c.foi_request_id)\
                      .where(FoiRequest.due_date < unres.c.max).subquery()
    
     late_all = select(func.coalesce(late_res.c.id, late_unres.c.id).label('id'))\
               .join(late_unres, late_res.c.id == late_unres.c.id, full=True).subquery()

     late = select(FoiRequest.campaign_id, func.count(late_all.c.id.distinct()))\
           .join(late_all, FoiRequest.id == late_all.c.id, isouter=True)\
           .group_by(FoiRequest.campaign_id).subquery()   
    
     late = select(late.c.campaign_id, case([(late.c.count.isnot(None), late.c.count)], else_=0).label('count')).subquery()

     if ascending:
         ordering = asc
     else:
         ordering = desc

     if s in ['Anzahl', 'Erfolgsquote', 'Verspaetungsquote']:
         stmt = select(Campaign.name, total_num.c.count.label('Anzahl'), (cast(resolved.c.count, Float)/total_num.c.count * 100).label('Erfolgsquote'), late.c.count.label('Fristüberschreitungen'), (cast(late.c.count, Float)/total_num.c.count * 100).label('Verspaetungsquote'))\
                  .join(resolved, Campaign.id == resolved.c.campaign_id)\
                  .join(total_num, Campaign.id == total_num.c.campaign_id)\
                  .join(late, late.c.campaign_id == Campaign.id)\
                  .where(total_num.c.campaign_id == resolved.c.campaign_id)\
                  .where(total_num.c.count>20)\
                  .order_by(ordering(s))\
                  .limit(10)   
     else:
         stmt = select(Campaign.name, total_num.c.count.label('Anzahl'), (cast(resolved.c.count, Float)/total_num.c.count * 100).label('Erfolgsquote'), late.c.count.label('Fristüberschreitungen'), (cast(late.c.count, Float)/total_num.c.count * 100).label('Verspaetungsquote'))\
                  .join(resolved, Campaign.id == resolved.c.campaign_id)\
                  .join(total_num, Campaign.id == total_num.c.campaign_id)\
                  .join(late, late.c.campaign_id == Campaign.id)\
                  .where(total_num.c.campaign_id == resolved.c.campaign_id)\
                  .where(total_num.c.count>20)\
                  .order_by('Verspaetungsquote')\
                  .limit(10)   
                
     print(stmt)                                         
     result = db.execute(stmt).fetchall()
     lst = []
     keys = list(dict(result[0]).keys())
     for row in result:
                dct = {}
                dct["name"] = str(row[keys[0]])
                dct["number"] = int(row[keys[1]])
                dct["success_rate"] = float(row[keys[2]])
                dct["number_overdue"] = int(row[keys[3]])
                dct["overdue_rate"] = float(row[keys[4]])
                lst.append(dct)   
    
     return lst


def query_ranking(db, typ, s, ascending, l = None):
    print(typ)
    if typ == "public_bodies":
        return {"ranking": ranking_public_body(db, s = s, ascending = ascending)}
    elif typ == "jurisdictions":
        return {"ranking": ranking_jurisdictions(db, s = s, ascending = ascending)}
    elif typ == "campaigns":
         return {"ranking": ranking_campaign(db, s = s, ascending = ascending)}