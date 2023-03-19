from rich.console import Console
import pandas as pd
from database import SessionLocal
from models import FoiRequest, Jurisdiction, Message, PublicBody
from queries import *
from sqlalchemy import text



def upload_jur(df, console):
    sess = SessionLocal()
    sess.execute(text(create_tmp_jurisdictions))
    console.print("Temporary table created.")
    
    try:
        data = df.to_numpy().tolist()
        for i in data:
            
            # update columns in case that here are changes to the column names
            record = Jurisdiction(**{
                "id": i[0],
                "name": i[1],
                "rank": i[2]
            })
            sess.add(record)

        sess.commit()
        console.print("Committed.")

        
        sess.execute(text(merge_jurisdiction))
        
    except:
        sess.rollback()
        console.print("Rollback.")
        raise
        
    
    finally:
        sess.execute(text(delete_tmp_jurisdictions)) # temporary table is deleted whether or not the update was successful
        sess.commit()
        console.print("Temporary table deleted.")
        sess.close()
        console.print("Session closed.")



def upload_foi(df, console):
    sess = SessionLocal()
    sess.execute(text(create_tmp_foi_requests))
    console.print("Temporary table created")
    
    try:
        data = df.to_numpy().tolist()
        for i in data:
            
            # update columns in case that here are changes to the column names
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
                "user_id": i[10],
                "public_body_id": i[11]
            })
            sess.add(record)
        
        sess.commit()
        console.print("Committed.")

        sess.execute(text(merge_foi_requests))

    except:
        sess.rollback()
        console.print("Rollback.")
        raise

    finally:
        sess.execute(text(delete_tmp_foi_requests)) # temporary table is deleted whether or not the update was successful
        sess.commit()
        console.print("Temporary table deleted.")
        sess.close()
        console.print("Session closed.")


def upload_message(df, console):
    sess = SessionLocal()
    sess.execute(text(create_tmp_messages))
    console.print("Temporary table created.")
    
    try:
        data = df.to_numpy().tolist()
        for i in data:
            
            # update columns in case that here are changes to the column names
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

        sess.execute(text(merge_messages))

    except:
        sess.rollback()
        console.print("Rollback.")
        raise

    finally:
        sess.execute(text(delete_tmp_messages))
        sess.commit()
        console.print("Temporary table deleted.") # temporary table is deleted whether or not the update was successful
        sess.close()
        console.print("Session closed.")



def upload_pb(df, console):
    sess = SessionLocal()
    sess.execute(text(create_tmp_public_bodies))
    console.print("Temporary table created.")
    
    try:
        data = df.to_numpy().tolist()
        for i in data:
            
            # update columns in case that here are changes to the column names
            record = PublicBody(**{
                "id": i[0],
                "name": i[1],
                "classification": i[2],
                "categories": i[3],
                "address": i[4],
                "jurisdiction": i[5]
            })
            sess.add(record)
            console.print("Record added.")

        sess.commit()
        console.print("Committed.")

        sess.execute(text(merge_public_bodies))
        
    except:
        sess.rollback()
        console.print("Rollback.")
        raise

    finally:
        sess.execute(text(delete_tmp_public_bodies))
        sess.commit()
        console.print("Temporary table deleted.") # temporary table is deleted whether or not the update was successful
        sess.close()
        console.print("Session closed.")