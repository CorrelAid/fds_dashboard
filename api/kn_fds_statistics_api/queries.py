from sqlalchemy.orm import Session
from kn_fds_statistics_api.models import FoiRequest
from kn_fds_statistics_api.query_text import *
from sqlalchemy import select, text
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


def total_group_by_count(db, column, table):
    query = f'''
    SELECT {column}, COUNT(*) 
    FROM {table}
    GROUP BY {column}
    '''
    return sql_to_dict(db, query)


def query_total_stats(db):
    return {"total_foi_requests": db.query(FoiRequest).count(),
            "total_users": sql_query(db, sql_total_users).scalar(),
            "total_dist_resolution": total_group_by_count(db, "resolution", "foi_requests"),
            "total_dist_status": total_group_by_count(db, "status", "foi_requests"),
            "total_requests_by_month": sql_to_dict(db, sql_total_requests_month, time_key=True)}


def query_general_info(db):
    return {"jurisdictions": sql_to_dict(db, sql_jurisdictions),
            "public_bodies": sql_to_dict(db, sql_public_bodies)}
    

def query_ranking(db):
    return {"public_bodies": sql_to_dict_lst(db, sql_ranking_pb),
            "jurisdictions": sql_to_dict_lst(db, sql_ranking_jurisdictions)}

    
