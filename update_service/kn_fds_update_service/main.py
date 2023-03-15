#from celery import Celery
from rich.console import Console
from sqlalchemy import create_engine,MetaData
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import TIMESTAMP
#from sqlalchemy.sql.expression import insert
from sqlalchemy import insert 
import psycopg2
from helpers import dload_update
from pp_update import pp_requests, pp_messages, pp_pb
from queries import *
from database import SessionLocal,engine,metadata
from models import FoiRequest, Jurisdiction, Message, PublicBody
import os 
import pandas as pd
import numpy as np
from sqlalchemy.exc import SQLAlchemyError

console=Console()

cols_foi_requests = ["id", "jurisdiction", "refusal_reason", "costs", "due_date", "resolved_on", "created_at", "last_message", "status", "resolution", "user", "public_body"]
cols_messages = ["id", "request", "sent", "is_response", "is_postal", "kind", "sender_public_body", "recipient_public_body", "status", "timestamp"]
cols_pbodies = ["id", "name", "classification", "categories", "address", "jurisdiction", ]


#celery=Celery('update-service',broker='', #insert broker backend='') #insert backend

#adjusted_config = 'kn_fds_update_service.celeryconfig'
#celery.config_from_object(adjusted_config)

#@celery.on_after_configue.connect
def setup_periodic_task():
    pass


#@app.task
def get_boundaries(db):
    # Query for latest date
    query_foi_requests = f'''
    SELECT last_message 
    FROM foi_requests 
    ORDER BY last_message DESC
    LIMIT 1
    '''
    #Query for messages
    query_messages = f'''
    SELECT timestamp
    FROM messages
    ORDER BY timestamp DESC
    LIMIT 1
    '''
    # Query for public bodies
    query_bodies = f'''
    SELECT id 
    FROM public_bodies
    ORDER BY id DESC
    LIMIT 1
    '''

    last_message=db.execute(text(query_foi_requests)).scalar()
    last_timestamp=db.execute(text(query_messages)).scalar()
    last_id = db.execute(text(query_bodies)).scalar()
    return last_message, last_timestamp, last_id
    #pass

def get_entries(latest_message, latest_timestamp, latest_id):
    # call update function from helpers.py
    dload_update("https://fragdenstaat.de/api/v1/request/", "foi_requests", "last_message", cols_foi_requests, latest_message, console)
    dload_update("https://fragdenstaat.de/api/v1/message/", "messages", "timestamp", cols_messages, latest_timestamp, console)
    dload_update("https://fragdenstaat.de/api/v1/publicbody/", "public_bodies", "id", cols_pbodies, latest_id, console)
    pass

def preprocessing():
    print("preprocessing requests...")
    pp_requests()
    print("preprocessing messages...")
    pp_messages()
    print("preprocessing public_bodies...")
    pp_pb()

def get_values():
    
    df_foi_requests = pd.read_csv("../data/update_foi_requests.csv")
    df_public_bodies = pd.read_csv("../data/update_public_bodies.csv")
    df_classifications = pd.read_csv("../data/update_classifications.csv")
    df_categories = pd.read_csv("../data/update_categories.csv")
    df_jurisdiction = pd.read_csv("../data/update_jurisdictions.csv")
    df_messages = pd.read_csv("../data/update_messages.csv")

    return df_foi_requests, df_public_bodies, df_classifications, df_categories, df_jurisdiction, df_messages

    #pass


def update_entries():
    # first session: get latest data (message, timestamp, id)
    session = SessionLocal()
    try:
        last_mess, last_times, last_id = get_boundaries(session)
    finally:
        session.close()
    
    # process data in order for upsert
    get_entries(last_mess, last_times, last_id)
    preprocessing()
    df_foi, df_pb, df_class, df_cat, df_jur, df_mes = get_values()
    
    # second session: upsert data
    session2 = SessionLocal()
    try:
        # general plan: 
        #   create temp table
        #   insert values into temp table
        #   merge with target table
        #   delete temp table

        session2.execute(create_tmp_jurisdictions)
        print("Temporary table 'tmp_jurisdictions' created")
        session2.execute(upsert_tmp_jurisdictions, df_jur.values.tolist())
        print("Data upserted to temporary table")
        session2.execute(merge_jurisdiction)
        print("Data merged")
        session2.execute(delete_tmp_jurisdictions)
        print("Temporary table deleted")

        session2.execute(create_tmp_public_bodies)
        print("Temporary table 'tmp_public_bodies' created")
        session2.execute(upsert_tmp_public_bodies, df_pb.values.tolist())
        print("Data upserted to temporary table")
        session2.execute(merge_public_bodies)
        print("Data merged")
        session2.execute(delete_tmp_public_bodies)
        print("Temporary table deleted")

        session2.execute(create_tmp_foi_requests)
        print("Temporary table 'tmp_foi_requests' created")
        session2.execute(upsert_tmp_foi_requests, df_foi.values.tolist())
        print("Data upserted to temporary table")
        session2.execute(merge_foi_requests)
        print("Data merged")
        session2.execute(delete_tmp_foi_requests)
        print("Temporary table deleted")

        session2.execute(create_tmp_messages)
        print("Temporary table 'tmp_messages' created")
        session2.execute(upsert_tmp_messages, df_mes.values.tolist())
        print("Data upserted to temporary table")
        session2.execute(merge_messages)
        print("Data merged")
        session2.execute(delete_tmp_messages)
        print("Temporary table deleted")


        


        
    
    finally:
        session2.close()
        print("Session2 closed.")



# TESTING

# Upsert new data into db



def upload_jur(df, console):
    sess = SessionLocal()
    sess.execute(text(create_tmp_jurisdictions))
    console.print("tmp table created")
    try:
        data = df.to_numpy().tolist()
        for i in data:
            record = Jurisdiction(**{
                "id": i[0],
                "name": i[1],
                "rank": i[2]
            })
            sess.add(record)

        sess.commit()
        console.print("Committed.")
    except SQLAlchemyError as e:
        sess.rollback()
        console.print("Rollback.")
        error = str(e.__dict__['orig'])
        console.print(error)
    
    finally:
        sess.close()
        console.print("Session closed.")

def upload_foi(df, console):
    sess = SessionLocal()
    sess.execute(text(create_tmp_foi_requests))
    console.print("Temporary table created")
    try:
        data = df.to_numpy().tolist()
        for i in data:
            record = FoiRequest(**{
                "id": i[0],
                "jurisdiction": i[1],
                "refusal_reason": i[2],
                "costs": i[3],
                "due_date": i[4],
                "resolved_on": i[5],
                "created_at": i[6],
                "last_message": i[7],
                "status": i[8],
                "resolution": i[9],
                "user": i[10],
                "public_body_id": i[11]
            })
            sess.add(record)
        
        sess.commit()
        console.print("Committed.")
    except SQLAlchemyError as e:
        sess.rollback()
        console.print("Rollback.")
        error = str(e.__dict__['orig'])
        console.print(error)

    finally:
        sess.close()
        console.print("Session closed.")

def upload_message(df, console):
    sess = SessionLocal()
    sess.execute(text(create_tmp_messages))
    console.print("Temporary table created.")
    try:
        data = df.to_numpy().tolist()
        for i in data:
            record = Message(**{
                "id": i[0],
                "request": i[1],
                "sent": i[2],
                "is_response": i[3],
                "is_postal": i[4],
                "kind": i[5],
                "sender_public_body": i[6],
                "recipient_public_body": i[7],
                "status": i[8],
                "timestamp": i[9]
            })
            sess.add(record)

        sess.commit()
        console.print("Committed.")
    except SQLAlchemyError as e:
        sess.rollback()
        console.print("Rollback.")
        error = str(e.__dict__['orig'])
        console.print(error)

    finally:
        sess.close()
        console.print("Session closed.")

def upload_pb(df, console):
    sess = SessionLocal()
    sess.execute(text(create_tmp_public_bodies))
    console.print("Temporary table created.")
    try:
        data = df.to_numpy().tolist()
        for i in data:
            record = PublicBody(**{
                "id": i[0],
                "name": i[1],
                "classification": i[2],
                "categories": i[3],
                "address": i[4],
                "jurisdiction": i[5]
            })
            sess.add(record)

        sess.commit()
        console.print("Committed.")

    except SQLAlchemyError as e:
        sess.rollback()
        console.print("Rollback.")
        error = str(e.__dict__['orig'])
        console.print(error)

    finally:
        sess.close()
        console.print("Session closed.")

df_foi, df_pb, df_class, df_cat, df_jur, df_mes = get_values()
#metadata.create_all(engine)
upload_jur(df_jur, console=console)
        



'''
df_foi, df_pb, df_class, df_cat, df_jur, df_mes = get_values()
#metadata.create_all(engine)
#jurtest = df_to_np_arr("../data/update_jurisdictions.csv")
jurtest = df_jur.to_numpy().tolist()
for i in jurtest:
    record = Jurisdiction(**{
        'id': i[0],
        'name': i[1],
        'rank': i[2]
    })
    console.print(record.id)
#console.print(jurtest)
'''


'''
df_foi, df_pb, df_class, df_cat, df_jur, df_mes = get_values()

metadata.create_all(engine)
df_jur.to_sql(con=engine, name=Jurisdiction.__tablename__, if_exists='replace', index=False)
'''
'''
df_foi, df_pb, df_class, df_cat, df_jur, df_mes = get_values()
with engine.begin() as con:
    con.execute(text(create_tmp_jurisdictions))
    console.print("Tmp table created")
    #con.execute(text("""INSERT INTO tmp_jurisdictions (id, name, rank) VALUES (%s, %s, %s)"""), df_jur.to_dict('records'))
    con.execute(text("""INSERT INTO tmp_jurisdictions (id, name, rank) VALUES (%s, %s, %s)"""), [(999, "JJ", 77)])
    console.print("Data inserted to tmp table")
    #con.execute(text(merge_jurisdiction))
    #console.print("data merged")
    #con.execute(text(delete_tmp_jurisdictions))
    #console.print("Tmp table deleted")
    
'''

'''
session2 = SessionLocal()
try:
    # general plan: 
    #   create temp table
    #   insert values into temp table
    #   merge with target table
    #   delete temp table

    session2.execute(text(create_tmp_jurisdictions))
    console.print("Temporary table 'tmp_jurisdictions' created")
    session2.execute(insert(tmp_jurisdictions), df_jur.to_dict('records'))
    console.print("Data upserted to temporary table")
    session2.execute(text(merge_jurisdiction))
    console.print("Data merged")
    session2.execute(text(delete_tmp_jurisdictions))
    console.print("Temporary table deleted")

    session2.execute(text(create_tmp_public_bodies))
    console.print("Temporary table 'tmp_public_bodies' created")
    session2.execute(text(upsert_tmp_public_bodies), df_pb.values.tolist())
    console.print("Data upserted to temporary table")
    session2.execute(text(merge_public_bodies))
    console.print("Data merged")
    session2.execute(text(delete_tmp_public_bodies))
    console.print("Temporary table deleted")

    session2.execute(text(create_tmp_foi_requests))
    console.print("Temporary table 'tmp_foi_requests' created")
    session2.execute(text(upsert_tmp_foi_requests), df_foi.values.tolist())
    console.print("Data upserted to temporary table")
    session2.execute(text(merge_foi_requests))
    console.print("Data merged")
    session2.execute(text(delete_tmp_foi_requests))
    console.print("Temporary table deleted")

    session2.execute(text(create_tmp_messages))
    console.print("Temporary table 'tmp_messages' created")
    session2.execute(text(upsert_tmp_messages), df_mes.values.tolist())
    console.print("Data upserted to temporary table")
    session2.execute(text(merge_messages))
    console.print("Data merged")
    session2.execute(text(delete_tmp_messages))
    console.print("Temporary table deleted")


    


    

finally:
    session2.close()
    console.print("Session2 closed.")

'''
# Preprocessing and df load

'''
preprocessing()
df_foi, df_pb, df_class, df_cat, df_jur, df_mes = get_values()
console.print(f"Number of rows in df_foi: {len(df_foi.index)}")
console.print(f"Number of rows in df_pb: {len(df_pb.index)}")
console.print(f"Number of rows in df_class: {len(df_class.index)}")
console.print(f"Number of rows in df_cat: {len(df_cat.index)}")
console.print(f"Number of rows in df_jur: {len(df_jur.index)}")
console.print(f"Number of rows in df_mes: {len(df_mes.index)}")
'''


# Boundary retrival and API request
'''
session = SessionLocal()
try:
    last_mess, last_times, last_id = get_boundaries(session)
finally:
    session.close()

get_entries(last_mess, last_times, last_id)
'''