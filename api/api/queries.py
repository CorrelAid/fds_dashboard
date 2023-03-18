from sqlalchemy.orm import Session
from sqlalchemy import func
from models import FoiRequest
from query_text import *
from sqlalchemy import select, text, MetaData, Table
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
         stmt = select(column, func.count(table.id)).where(table.public_body_id == s).group_by(column)
    else:
         stmt = select(column, func.count(table.id)).group_by(column)
    result = db.execute(stmt).fetchall()
    result = [tuple(row) for row in result]
    return result

def requests_by_month(db, table, column, l, s):
    if l != None and s != None:
            stmt = select(func.date_trunc("month", column), func.count(table.id))\
            .where(table.public_body_id == s)\
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
     if l != None and s != None:
          stmt = select(func.count(table.user_id.distinct())).where(table.public_body_id == s)
     else:
          stmt = select(func.count(table.user_id.distinct()))
     result = db.execute(stmt).fetchall()
     result = [tuple(row) for row in result]
     return result[0][0]

def request_count(db, table, l, s):
     if l != None and s != None:
          stmt = select(func.count(table.id.distinct())).where(table.public_body_id == s)
     else:
          stmt = select(func.count(table.id.distinct()))
     result = db.execute(stmt).fetchall()
     result = [tuple(row) for row in result]
     return result[0][0]

 
def query_stats(db, l, s):
    return {"stats_foi_requests": request_count(db, FoiRequest, l=l, s=s),
            "stats_users": user_count(db, FoiRequest, l=l, s=s),
            "stats_dist_resolution": group_by_count(db, FoiRequest, FoiRequest.resolution, l=l, s=s),
            "stats_dist_status": group_by_count(db, FoiRequest, FoiRequest.status, l=l, s=s),
            "stats_requests_by_month": requests_by_month(db, FoiRequest, FoiRequest.first_message, l=l, s=s)}


def query_general_info(db, l = None, s = None):
    return {"jurisdictions": sql_to_dict(db, sql_jurisdictions),
            "public_bodies": sql_to_dict(db, sql_public_bodies)}
    

def query_ranking_public_body(db, l = None, s = None):
    return {"public_bodies": sql_to_dict_lst(db, sql_ranking_pb)}

def query_ranking_jurisdiction(db, l = None, s = None):
    return {"jurisdictions": sql_to_dict_lst(db, sql_ranking_jurisdictions)}

    
