import pandas as pd
import requests
from datetime import datetime
from rich.console import Console
from rich.status import Status
from sys import exit
from helpercode.helpers import make_rel_path, decompress_pickle, compressed_pickle, convert_time_str, get_item

console = Console()

console.print("Hello :smiley:")
console.rule("")

with Status("decompressing...") as status:
    df = decompress_pickle(make_rel_path("data/foi_request_list.pbz2"))

old_df_len = df.shape[0]

url = "https://fragdenstaat.de/api/v1/request/"

offset = 0
all_objects = []
done = False

# newest request
last_time = df.iloc[0]["last_message"]

with Status("Updating...") as status:
    while done == False:
        query = {"limit": 50, "offset": offset}

        try:    
                res = requests.get(url, params=query,
                        headers={'content-type': 'application/json'
                                },
                        )
                res.raise_for_status()

        # Error Handling: printing error, current offset 
        except requests.exceptions.HTTPError as error:
                console.log(error)
                exit(0) #exit script
        
        df_new = pd.DataFrame(res.json()["objects"])
        
        index = df_new.shape[0]-1 #index in currently requested list if all requested objects are not in the already saved list

        # sorting by last message to be able to compare the result of request with already existing list
        df_new.sort_values(by="last_message", ascending=False, inplace=True)
        
        status.update(status="Converting to datetime")
        df_new["last_message"] = pd.to_datetime(df_new.last_message)

        status.update(status="Filtering")
        # deleting all new requests that are older than newest of already existent list
        filtered_df = df_new.loc[(df_new['last_message'] > last_time)]
        
        status.update(status="Concatenating...")
        df = pd.concat([filtered_df, df]) #first filtered, then old df

        # because offset is 50, if the filtered df is smaller, we already reached beginning of already existing list
        if filtered_df.shape[0] < 50:
            done = True
        
        offset += 50

console.print("added {x} foi_requests, length is now {y}. Previously. {z}".format(x=filtered_df.shape[0], y=df.shape[0], z=old_df_len))


#pickling (serializing), compressing and saving resulting list    
with Status("Compressing...") as status:
        compressed_pickle(make_rel_path("data/foi_request_list.pbz2"), df)
        
console.rule("")

console.print("Done!")
