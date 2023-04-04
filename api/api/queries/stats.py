from sqlalchemy.orm import Session
from sqlalchemy import func
from models import FoiRequest, PublicBody, Jurisdiction, Campaign, Message
from sqlalchemy import select, text, MetaData, Table, asc, desc, cast, DECIMAL, Float, literal, case
from datetime import datetime

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
#     for row in result:
#      print(row[0])
    result = [{"value": row[1], "name": row[0]} for row in result]
#     print(result)
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
    resolved_mess = select(Message.foi_request_id.distinct().label('foi_request_id'))\
                           .where(Message.status == 'resolved').subquery()

    res_date = select(Message.foi_request_id, func.min(Message.timestamp))\
                      .filter(Message.foi_request_id.in_(resolved_mess))\
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
    
    late = select(func.coalesce(late_res.c.id, late_unres.c.id).label('id'))\
               .join(late_unres, late_res.c.id == late_unres.c.id, full=True).subquery()
    
    if l == None and s == None:
         stmt = select(func.count(FoiRequest.id.distinct()).label('Anzahl'), cast(func.count(resolved_mess.c.foi_request_id), Float).label('Anzahl_Erfolgreich'), cast(func.count(late.c.id), Float).label('Fristueberschreitungen'))\
                  .select_from(FoiRequest)\
                  .join(late, late.c.id == FoiRequest.id, isouter=True)\
                  .join(resolved_mess, FoiRequest.id == resolved_mess.c.foi_request_id, isouter=True).subquery()
    
         final = select(stmt.c.Anzahl.label('Anzahl'), (stmt.c.Anzahl_Erfolgreich / stmt.c.Anzahl * 100).label('Erfolgsquote'), stmt.c.Fristueberschreitungen, (stmt.c.Fristueberschreitungen / stmt.c.Anzahl * 100).label('Verspätungsquote'))
   
    elif l == 'public_body':
         stmt =  select(func.count(FoiRequest.id.distinct()).label('Anzahl'), cast(func.count(resolved_mess.c.foi_request_id), Float).label('Anzahl_Erfolgreich'), cast(func.count(late.c.id), Float).label('Fristueberschreitungen'))\
                  .join(resolved_mess, FoiRequest.id == resolved_mess.c.foi_request_id, isouter=True)\
                  .join(late, late.c.id == FoiRequest.id, isouter=True)\
                  .where(FoiRequest.public_body_id == s)
         
         final = select(stmt.c.Anzahl.label('Anzahl'), (stmt.c.Anzahl_Erfolgreich / stmt.c.Anzahl * 100).label('Erfolgsquote'), stmt.c.Fristueberschreitungen, (stmt.c.Fristueberschreitungen / stmt.c.Anzahl * 100).label('Verspätungsquote'))

    elif l == 'jurisdiction':
         print('here')
         stmt =  select(func.count(FoiRequest.id.distinct()).label('Anzahl'), cast(func.count(resolved_mess.c.foi_request_id), Float).label('Anzahl_Erfolgreich'), cast(func.count(late.c.id), Float).label('Fristueberschreitungen'))\
                  .join(resolved_mess, FoiRequest.id == resolved_mess.c.foi_request_id, isouter=True)\
                  .join(late, late.c.id == FoiRequest.id, isouter=True)\
                  .where(FoiRequest.jurisdiction == s)
         
         final = select(stmt.c.Anzahl.label('Anzahl'), (stmt.c.Anzahl_Erfolgreich / stmt.c.Anzahl * 100).label('Erfolgsquote'), stmt.c.Fristueberschreitungen, (stmt.c.Fristueberschreitungen / stmt.c.Anzahl * 100).label('Verspätungsquote'))
    else:
         stmt =  select(func.count(FoiRequest.id.distinct()).label('Anzahl'), cast(func.count(resolved_mess.c.foi_request_id), Float).label('Anzahl_Erfolgreich'), cast(func.count(late.c.id), Float).label('Fristueberschreitungen'))\
                  .join(resolved_mess, FoiRequest.id == resolved_mess.c.foi_request_id, isouter=True)\
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
    return {"foi_requests": request_count(db, FoiRequest, l=l, s=s),
            "users": user_count(db, FoiRequest, l=l, s=s),
            "dist_resolution": group_by_count(db, FoiRequest, FoiRequest.resolution, l=l, s=s),
            "dist_status": group_by_count(db, FoiRequest, FoiRequest.status, l=l, s=s),
            "requests_by_month": requests_by_month(db, FoiRequest, FoiRequest.created_at, l=l, s=s),
            "percentage_costs": percentage_costs(db, l=l, s=s),
            "success_rate": overall_rates(db, l=l, s=s)}