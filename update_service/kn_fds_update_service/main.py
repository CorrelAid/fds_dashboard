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
from helpers import get_boundaries, get_entries#, preprocessing, get_values
from pp_update import pp_requests, pp_messages, pp_pb
from queries import *
from database import SessionLocal,engine,metadata
from models import FoiRequest, Jurisdiction, Message, PublicBody
from upload import upload_foi, upload_jur, upload_message, upload_pb
import os 
import pandas as pd
import numpy as np
from sqlalchemy.exc import SQLAlchemyError
from time import time

console=Console()

cols_foi_requests = ["id", "jurisdiction", "refusal_reason", "costs", "due_date", "resolved_on", "created_at", "last_message", "status", "resolution", "user", "public_body"]
cols_messages = ["id", "request", "sent", "is_response", "is_postal", "kind", "sender_public_body", "recipient_public_body", "status", "timestamp"]
cols_pbodies = ["id", "name", "classification", "categories", "address", "jurisdiction"]


#celery=Celery('update-service',broker='', #insert broker backend='') #insert backend

#adjusted_config = 'kn_fds_update_service.celeryconfig'
#celery.config_from_object(adjusted_config)

#@celery.on_after_configue.connect
def setup_periodic_task():
    pass


#@app.task



def update_entries(cols_foi_requests, cols_messages, cols_pbodies, console):
    # get latest data (message, timestamp, id)
    session = SessionLocal()
    try:
        last_mess, last_times, last_id = get_boundaries(session)
    finally:
        session.close()
    
    # collect new data in .pbz2 files if exists, returns bool indicating if so
    new_foi_request, new_message, new_public_body = get_entries(cols_foi_requests, cols_messages, cols_pbodies, last_mess, last_times, last_id, console)
    
    # if new data found, start preprocessing and upload
    # preprocessing: storing data in csvs

    if new_foi_request:
        console.print("Preprocessing requests...")
        pp_requests()

        df_foi_requests = pd.read_csv("../data/update_foi_requests.csv")
        upload_foi(df_foi_requests, console=console)
        
    if new_message:
        console.print("Preprocessing messages...")
        pp_messages()

        df_messages = pd.read_csv("../data/update_messages.csv")
        upload_message(df_messages, console=console)

    if new_public_body:
        console.print("Preprocessing public_bodies...")
        pp_pb()

        df_public_bodies = pd.read_csv("../data/update_public_bodies.csv")
        df_classifications = pd.read_csv("../data/update_classifications.csv")
        df_categories = pd.read_csv("../data/update_categories.csv")
        df_jurisdiction = pd.read_csv("../data/update_jurisdictions.csv")

        upload_pb(df_public_bodies, console=console)
        upload_jur(df_jurisdiction, console=console)
    
    
    '''
    preprocessing()
    
    df_foi, df_pb, df_class, df_cat, df_jur, df_mes = get_values()
    
    upload_foi(df_foi, console=console)
    upload_jur(df_jur, console=console)
    upload_message(df_mes, console=console)
    upload_pb(df_pb, console=console)
    '''













# TESTING

# Overall process test run

t = time()
update_entries(cols_foi_requests, cols_messages, cols_pbodies, console=console)
t2= time()
console.print("Time taken for whole process: {}".format((t2-t)//3600))
#console.print("Time taken for whole process: {}".format(t2-t))


# Upsert new data into db



#df_foi, df_pb, df_class, df_cat, df_jur, df_mes = get_values()

#upload_jur(df_jur, console=console)
        


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