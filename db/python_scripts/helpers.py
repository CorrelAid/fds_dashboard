import pathlib
import bz2
import _pickle as cPickle
from datetime import datetime
import requests
from sys import exit
import math
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

##### Based on https://betterprogramming.pub/load-fast-load-big-with-compressed-pickles-5f311584507e #####

def compressed_pickle(path, data):
 with bz2.BZ2File(path, "w") as f: 
    cPickle.dump(data, f)
 
def decompress_pickle(path):
    data = bz2.BZ2File(path, "rb")
    data = cPickle.load(data)
    return data

##########################################################################################################

def dload(url:str,type:str,sort_by:str, keep_cols:list, console):
        # sending an initial request to retreive total count
        initial_query = {"limit": 50, "offset": None}
        initial_res = requests.get(url, params=initial_query,
                        headers={'content-type': 'application/json'
                                },
                        )
        
        total = initial_res.json()["meta"]["stats_count"]

        # Calculating max offset and number of needed requests
        fifties = math.ceil(total/50)
        console.print(f"Total count: [bold green]{fifties}[/bold green]. We have to send [bold green]{total}[/bold green] requests.")
        max_offset = total - 50

        console.rule("")

        all_objects = []
        offset = total-50
        i = 1
        stats_adjust = 0
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
                        
                        updated_total = res.json()["meta"]["stats_count"]

                        all_objects += res.json()["objects"]
                        
                        adjustment = updated_total - current_total
                        
                        current_total = updated_total
                
                        console.log(f"Request: {i} of {fifties}. Current Offset: {offset}, Current total: {current_total}, Started with a total of: {total}")
                
                # Error Handling: printing error, current offset and saving interim result
                except Exception as e:
                        console.rule("")
                        console.log(e)
                        console.rule("")
                        console.log("Error occured at request: {x} of {y}. Current Offset: {z}".format(x=i, y=fifties, z=offset))
                        
                        
                        df = pd.DataFrame(all_objects)
                        # sorting to be able to update based on last message in separate script
                        df.sort_values(by=sort_by, ascending=False, inplace=True)
                        compressed_pickle(f"data/{type}_failed.pbz2", df)
                        exit(1) #exit script signaling failure
                i += 1

                # handling the case that new requests were added while running script
                if adjustment > 0:
                        console.print("Adjustment of offset by {x} required, because new data was added.".format(x=adjustment))
                
                offset += adjustment
                stats_adjust += adjustment
                
                # if adjustment greater than limit
                if stats_adjust > 50:
                        fifties += 1
                        console.print("Number of requests increased. Resetting stats_adjust")
                        stats_adjust = 0
                
                # decreasing offset
                if offset > 0:
                        console.print("Decreasing offset")
                        offset -= 50 
                

        console.print(f"Number of downloaded items: {len(all_objects)}. FDS has {current_total} items in its database.")

        
        df = pd.DataFrame(all_objects)
        # sorting to be able to update based on last message in separate script
        console.print("Sorting...")
        df.sort_values(by=sort_by, ascending=False, inplace=True)

        # with Status("Converting last_message to datetime...") as status:
        #         df["last_message"] = pd.to_datetime(df.last_message)

        # pickling (serializing), compressing and saving df
        console.print("Deleting not specified columns...")
        df = df[keep_cols]
      
        compressed_pickle(f"data/{type}.pbz2", df)

        