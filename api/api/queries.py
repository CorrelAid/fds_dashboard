from sqlalchemy.orm import Session
from sqlalchemy import func
from models import FoiRequest, PublicBody, Jurisdiction, Campaign, Message
from query_text import *
from sqlalchemy import select, text, MetaData, Table, asc, desc, cast, DECIMAL, Float, literal, case
from datetime import datetime

def sql_query(db, query):
    return db.execute(text(query))


def sql_to_dict(db, query, time_key=False, ranking=False):
    dct = {}
    result = sql_query(db, query).all()
    keys = list(dict(result[0]).keys())
    if time_key:
        for row in result:
            time = row[keys[0]].strftime("%Y-%m")
            dct[time] = row[keys[1]]
    else: 
        for row in result:
            print(row)
            dct[str(row[keys[0]])] = row[keys[1]]
    return dct

def sql_to_dict_lst(db, query):
    lst = []
    result = sql_query(db, query).all()
    keys = list(dict(result[0]).keys())
    for row in result:
                print(row)
                dct = {}
                dct["name"] = str(row[keys[0]])
                dct["number"] = int(row[keys[1]])
                dct["success_rate"] = float(row[keys[2]])
                dct["number_overdue"] = int(row[keys[3]])
                dct["overdue_rate"] = float(row[keys[4]])
                lst.append(dct)    
    return lst


def sql_to_list(db, query):
    result = [str(x[0]) for x in sql_query(db, query) if None not in x]
    return result

def group_by_count(db, table, column, l, s):
    if l != None and s != None:
        # metadata = MetaData()
        # table2 = Table(table, metadata, autoload=True, autoload_with=db)
        # column2 = getattr(table2.c, l); getattr(table.columns, l)
        if l == 'public_body':
            stmt = select(column, func.count(table.id)).where(table.public_body_id == s).group_by(column)
        elif l == 'jurisdiction':
            stmt = select(column, func.count(table.id)).where(table.jurisdiction == s).group_by(column)
        else:
             stmt = select(column, func.count(table.id)).where(table.campaign == s).group_by(column)
    else:
         stmt = select(column, func.count(table.id)).group_by(column)
    result = db.execute(stmt).fetchall()
    result = [tuple(row) for row in result]
    return result

def requests_by_month(db, table, column, l, s):
    if l == 'public_body':
            stmt = select(func.date_trunc("month", column), func.count(table.id))\
            .where(table.public_body_id == s)\
            .group_by(func.date_trunc("month", column))\
            .order_by(func.date_trunc("month", column))
    elif l == 'jurisdiction':
         stmt = select(func.date_trunc("month", column), func.count(table.id))\
            .where(table.jurisdiction == s)\
            .group_by(func.date_trunc("month", column))\
            .order_by(func.date_trunc("month", column))         
    else:
         stmt = select(func.date_trunc("month", column), func.count(table.id))\
         .group_by(func.date_trunc("month", column))\
         .order_by(func.date_trunc("month", column))
    result = db.execute(stmt).fetchall()
    result = [tuple(row) for row in result]
    return result

def user_count(db, table, l, s):
     if l == 'public_body':
          stmt = select(func.count(table.user_id.distinct())).where(table.public_body_id == s)
     elif l == 'jurisdiction':
          stmt = select(func.count(table.user_id.distinct())).where(table.jurisdiction == s)
     else:
          stmt = select(func.count(table.user_id.distinct()))
     result = db.execute(stmt).fetchall()
     result = [tuple(row) for row in result]
     return result[0][0]

def request_count(db, table, l, s):
     if l == 'public_body':
          stmt = select(func.count(table.id.distinct())).where(table.public_body_id == s)
     elif l == 'jurisdiction':
        stmt = select(func.count(table.id.distinct())).where(table.jurisdiction == s)
     else:
          stmt = select(func.count(table.id.distinct()))
     result = db.execute(stmt).fetchall()
     result = [tuple(row) for row in result]
     return result[0][0]

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

def ranking(db):
    total_num = select(FoiRequest.public_body_id, func.count(FoiRequest.id.distinct()))\
                        .where(FoiRequest.public_body_id != None)\
                        .group_by(FoiRequest.public_body_id).subquery()

    resolved_mess = select(Message.request.distinct())\
                           .where(Message.status == 'resolved').subquery()

    resolved = select(FoiRequest.public_body_id, func.count(FoiRequest.id.distinct()))\
                      .where(FoiRequest.public_body_id != None)\
                      .filter(FoiRequest.id.in_(resolved_mess))\
                      .group_by(FoiRequest.public_body_id).subquery()

    res_date = select(Message.request, func.min(Message.timestamp))\
                      .where(Message.status == 'resolved')\
                      .group_by(Message.request).subquery()

    unres = select(Message.request, func.max(Message.timestamp))\
                   .filter(~Message.request.in_(resolved_mess))\
                   .group_by(Message.request).subquery()
    
    late_res = select(FoiRequest.id)\
                      .join(res_date, FoiRequest.id == res_date.c.request)\
                      .where(FoiRequest.due_date < res_date.c.min).subquery()

    late_unres = select(FoiRequest.id)\
                      .join(unres, FoiRequest.id == unres.c.request)\
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
                print(row)
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
                  .join(PublicBody, Jurisdiction.id == PublicBody.jurisdiction)\
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
                print(row)
                dct = {}
                dct["name"] = str(row[keys[0]])
                dct["number"] = int(row[keys[1]])
                dct["success_rate"] = float(row[keys[2]])
                dct["number_overdue"] = int(row[keys[3]])
                dct["overdue_rate"] = float(row[keys[4]])
                lst.append(dct)    
    return lst

def percentage_costs(db, l, s):
    if l == None and s == None:
         not_free = select(FoiRequest.id).where(FoiRequest.costs != 0.0).subquery()
         stmt = select(func.count(not_free.c.id.distinct())/(cast(func.count(FoiRequest.id.distinct()), Float))*100)\
                  .join(not_free, not_free.c.id ==FoiRequest.id, isouter=True)
    else:
         if l == 'public_body':
              not_free = select(FoiRequest.id).where(FoiRequest.costs != 0.0).where(FoiRequest.public_body_id == s).subquery()
              stmt = select(func.count(not_free.c.id.distinct())/(cast(func.count(FoiRequest.id.distinct()), Float))*100)\
                  .join(not_free, not_free.c.id ==FoiRequest.id, isouter=True).where(FoiRequest.public_body_id == s)
         else:
              not_free = select(FoiRequest.id).where(FoiRequest.costs != 0.0).where(FoiRequest.jurisdiction == s).subquery()
              stmt = select(func.count(not_free.c.id.distinct())/(cast(func.count(FoiRequest.id.distinct()), Float))*100)\
                  .join(not_free, not_free.c.id ==FoiRequest.id, isouter=True).where(FoiRequest.jurisdiction == s)
    result = db.execute(stmt).fetchall()
    result = [tuple(row) for row in result]
    return result[0][0]

def overall_rates(db, l, s):
    resolved_mess = select(Message.request.distinct().label('request'))\
                           .where(Message.status == 'resolved').subquery()

    res_date = select(Message.request, func.min(Message.timestamp))\
                      .filter(Message.request.in_(resolved_mess))\
                      .group_by(Message.request).subquery()

    unres = select(Message.request, func.max(Message.timestamp))\
                   .filter(~Message.request.in_(resolved_mess))\
                   .group_by(Message.request).subquery()
    
    late_res = select(FoiRequest.id)\
                      .join(res_date, FoiRequest.id == res_date.c.request)\
                      .where(FoiRequest.due_date < res_date.c.min).subquery()

    late_unres = select(FoiRequest.id)\
                      .join(unres, FoiRequest.id == unres.c.request)\
                      .where(FoiRequest.due_date < unres.c.max).subquery()
    
    late = select(func.coalesce(late_res.c.id, late_unres.c.id).label('id'))\
               .join(late_unres, late_res.c.id == late_unres.c.id, full=True).subquery()
    
    if l == None and s == None:
         stmt = select(func.count(FoiRequest.id.distinct()).label('Anzahl'), cast(func.count(resolved_mess.c.request), Float).label('Anzahl_Erfolgreich'), cast(func.count(late.c.id), Float).label('Fristueberschreitungen'))\
                  .select_from(FoiRequest)\
                  .join(late, late.c.id == FoiRequest.id, isouter=True)\
                  .join(resolved_mess, FoiRequest.id == resolved_mess.c.request, isouter=True).subquery()
    
         final = select(stmt.c.Anzahl.label('Anzahl'), (stmt.c.Anzahl_Erfolgreich / stmt.c.Anzahl * 100).label('Erfolgsquote'), stmt.c.Fristueberschreitungen, (stmt.c.Fristueberschreitungen / stmt.c.Anzahl * 100).label('Verspätungsquote'))
   
    elif l == 'public_body':
         stmt =  select(func.count(FoiRequest.id.distinct()).label('Anzahl'), cast(func.count(resolved_mess.c.request), Float).label('Anzahl_Erfolgreich'), cast(func.count(late.c.id), Float).label('Fristueberschreitungen'))\
                  .join(resolved_mess, FoiRequest.id == resolved_mess.c.request, isouter=True)\
                  .join(late, late.c.id == FoiRequest.id, isouter=True)\
                  .where(FoiRequest.public_body_id == s)
         
         final = select(stmt.c.Anzahl.label('Anzahl'), (stmt.c.Anzahl_Erfolgreich / stmt.c.Anzahl * 100).label('Erfolgsquote'), stmt.c.Fristueberschreitungen, (stmt.c.Fristueberschreitungen / stmt.c.Anzahl * 100).label('Verspätungsquote'))

    elif l == 'jurisdiction':
         print('here')
         stmt =  select(func.count(FoiRequest.id.distinct()).label('Anzahl'), cast(func.count(resolved_mess.c.request), Float).label('Anzahl_Erfolgreich'), cast(func.count(late.c.id), Float).label('Fristueberschreitungen'))\
                  .join(resolved_mess, FoiRequest.id == resolved_mess.c.request, isouter=True)\
                  .join(late, late.c.id == FoiRequest.id, isouter=True)\
                  .where(FoiRequest.jurisdiction == s)
         
         final = select(stmt.c.Anzahl.label('Anzahl'), (stmt.c.Anzahl_Erfolgreich / stmt.c.Anzahl * 100).label('Erfolgsquote'), stmt.c.Fristueberschreitungen, (stmt.c.Fristueberschreitungen / stmt.c.Anzahl * 100).label('Verspätungsquote'))
    else:
         stmt =  select(func.count(FoiRequest.id.distinct()).label('Anzahl'), cast(func.count(resolved_mess.c.request), Float).label('Anzahl_Erfolgreich'), cast(func.count(late.c.id), Float).label('Fristueberschreitungen'))\
                  .join(resolved_mess, FoiRequest.id == resolved_mess.c.request, isouter=True)\
                  .join(late, late.c.id == FoiRequest.id, isouter=True)\
                  .where(FoiRequest.campaign == s)
         
         final = select(stmt.c.Anzahl.label('Anzahl'), (stmt.c.Anzahl_Erfolgreich / stmt.c.Anzahl * 100).label('Erfolgsquote'), stmt.c.Fristueberschreitungen, (stmt.c.Fristueberschreitungen / stmt.c.Anzahl * 100).label('Verspätungsquote'))
   
    result = db.execute(final).fetchall()
    print("result: ")
    print(result)
    dct = {}

    dct["number"] = float(result[0][0])
    dct["success_rate"] = float(result[0][1])
    dct["number overdue"] = float(result[0][2])
    dct["overdue_rate"] = float(result[0][3])
    return dct

def query_stats(db, l, s, ascending = None):
    return {"stats_foi_requests": request_count(db, FoiRequest, l=l, s=s),
            "stats_users": user_count(db, FoiRequest, l=l, s=s),
            "stats_dist_resolution": group_by_count(db, FoiRequest, FoiRequest.resolution, l=l, s=s),
            "stats_dist_status": group_by_count(db, FoiRequest, FoiRequest.status, l=l, s=s),
            "stats_requests_by_month": requests_by_month(db, FoiRequest, FoiRequest.first_message, l=l, s=s),
            "stats_percentage_costs": percentage_costs(db, l=l, s=s),
            "stats_success_rate": overall_rates(db, l=l, s=s)}


def query_general_info(db, l = None, s = None, ascending = None):
    return {"jurisdictions": drop_down_options(db, Jurisdiction),
            "public_bodies": drop_down_options(db, PublicBody),
            "campaign_starts": campaign_start_dates(db)}
    
def query_ranking_public_body(db, s, ascending, l = None):
    return {"public_bodies": ranking_public_body(db, s = s, ascending = ascending)}

def query_ranking_jurisdiction(db, ascending, s, l = None):
    return {"jurisdictions": ranking_jurisdictions(db, s = s, ascending = ascending)}
