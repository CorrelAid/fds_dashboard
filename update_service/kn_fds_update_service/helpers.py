import pathlib
import bz2
import _pickle as cPickle
from datetime import datetime
import requests
from sys import exit
import math
import pandas as pd
import pytz
from sqlalchemy import text
from rich.console import Console
from pp_update import pp_requests, pp_messages, pp_pb
import pandas as pd

def convert_time_str(str):
     # time string format varies. sometimes with miliseconds, sometimes without
    if '.' not in str:
        time = datetime.strptime(str, '%Y-%m-%dT%H:%M:%S%z')
    else:
        time = datetime.strptime(str, '%Y-%m-%dT%H:%M:%S.%f%z')
    return time

def get_item(collection, key, target):
     return next((item for item in collection if item[key] == target), None)

##########################################################################################################
# HELPER FUNCTIONS FOR UPDATE

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

def get_entries(cols_foi_requests, cols_messages, cols_pbodies, latest_message, latest_timestamp, latest_id, console):
    # call update function from helpers.py
    new_foi = dload_update("https://fragdenstaat.de/api/v1/request/", "foi_requests", "last_message", cols_foi_requests, latest_message, console)
    new_mess = dload_update("https://fragdenstaat.de/api/v1/message/", "messages", "timestamp", cols_messages, latest_timestamp, console)
    new_pbodies = dload_update("https://fragdenstaat.de/api/v1/publicbody/", "public_bodies", "id", cols_pbodies, latest_id, console)
    return new_foi, new_mess, new_pbodies

def preprocessing(console):
    console.print("preprocessing requests...")
    pp_requests()
    console.print("preprocessing messages...")
    pp_messages()
    console.print("preprocessing public_bodies...")
    pp_pb()

def get_values():
    
    df_foi_requests = pd.read_csv("../data/update_foi_requests.csv")
    df_public_bodies = pd.read_csv("../data/update_public_bodies.csv")
    df_classifications = pd.read_csv("../data/update_classifications.csv")
    df_categories = pd.read_csv("../data/update_categories.csv")
    df_jurisdiction = pd.read_csv("../data/update_jurisdictions.csv")
    df_messages = pd.read_csv("../data/update_messages.csv")

    return df_foi_requests, df_public_bodies, df_classifications, df_categories, df_jurisdiction, df_messages

########################################################################################################## 

##### Based on https://betterprogramming.pub/load-fast-load-big-with-compressed-pickles-5f311584507e #####

def compressed_pickle(path, data):
 with bz2.BZ2File(path, "w") as f: 
    cPickle.dump(data, f)
 
def decompress_pickle(path):
    data = bz2.BZ2File(path, "rb")
    data = cPickle.load(data)
    return data

##########################################################################################################

# fomer dload() function that has been adapted for updates
def dload_update(url:str,type:str,sort_by:str, keep_cols:list, boundary, console):  
        # sending an initial request to retreive total count
        initial_query = {"limit": 50, "offset": None}
        initial_res = requests.get(url, params=initial_query,
                        headers={'content-type': 'application/json'
                                },
                        )
        
        total = initial_res.json()["meta"]["total_count"]

        # Calculating max offset and number of needed requests
        fifties = math.ceil(total/50)
        console.print(f"Total count: [bold green]{fifties}[/bold green]. We have to send [bold green]{total}[/bold green] requests.")
        max_offset = total - 50

        console.rule("")

        new_objects = []
        offset = total-50
        i = 1
        total_adjust = 0
        current_total=total
        
        while offset != 0:
                adjustment = 0
                if offset < 0:
                        offset = 0
                        console.print("offset below zero, setting to zero")

                query = {"limit": 50, "offset": offset}
                
                try:    
                        res = requests.get(url, params=query,
                                headers={'content-type': 'application/json'
                                        },
                                )
                        res.raise_for_status()
                        
                        updated_total = res.json()["meta"]["total_count"]

                        #all_objects += res.json()["objects"]
                        #current_objects = []
                        current_objects = res.json()["objects"]
                        #print(current_objects)

                        for _entry in current_objects:
                                
                                #print(_entry)
                                sorting_val = _entry[sort_by]

                                if isinstance(boundary, datetime):
                                      sorting_val = convert_time_str(sorting_val)

                                      boundary_tzi = pytz.utc.localize(boundary)

                                      if sorting_val <= boundary_tzi:
                                            continue
                                      else:
                                            new_objects.append(_entry)
                                            #print("New entry found")
                                
                                else: 
                                      if sorting_val <= boundary:
                                            continue
                                      else: 
                                            new_objects.append(_entry)
                                            #print("New object founds")
         

                        adjustment = updated_total - current_total
                        
                        current_total = updated_total
                
                        console.log(f"Request: {i} of {fifties}. Current Offset: {offset}, Current total: {current_total}, Started with a total of: {total}")
                
                # Error Handling: printing error, current offset and saving interim result
                except Exception as e:
                        console.rule("")
                        console.log(e)
                        console.rule("")
                        console.log("Error occured at request: {x} of {y}. Current Offset: {z}".format(x=i, y=fifties, z=offset))
                        
                        
                        df = pd.DataFrame(new_objects)
                        # sorting to be able to update based on last message in separate script
                        df.sort_values(by=sort_by, ascending=False, inplace=True)
                        compressed_pickle(f"data/{type}_failed.pbz2", df)
                        exit(1) #exit script signaling failure
                i += 1

                # handling the case that new requests were added while running script
                if adjustment > 0:
                        console.print("Adjustment of offset by {x} required, because new data was added.".format(x=adjustment))
                
                offset += adjustment
                total_adjust += adjustment
                
                # if adjustment greater than limit
                if total_adjust > 50:
                        fifties += 1
                        console.print("Number of requests increased. Resetting total_adjust")
                        total_adjust = 0
                
                # decreasing offset
                if offset > 0:
                        console.print("Decreasing offset")
                        offset -= 50 
                
                #print(len(new_objects))
                #print(new_objects)
                #break

        console.print(f"Number of downloaded items: {len(new_objects)}. FDS has {current_total} items in its database.")

        if len(new_objects)>0:
                
                df = pd.DataFrame(new_objects)
                # sorting to be able to update based on last message in separate script
                console.print("Sorting...")
                df.sort_values(by=sort_by, ascending=False, inplace=True)

                # with Status("Converting last_message to datetime...") as status:
                #         df["last_message"] = pd.to_datetime(df.last_message)

                # pickling (serializing), compressing and saving df
                console.print("Deleting not specified columns...")
                df = df[keep_cols]
        
                compressed_pickle(f"../data/update_{type}.pbz2", df)

                return True

        else: 
                console.print("No new entries found.")
                
                return False