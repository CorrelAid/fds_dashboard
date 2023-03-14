import pandas as pd
from rich.console import Console
from rich.status import Status
from helpers import decompress_pickle, compressed_pickle

console = Console()

def pp_requests():
    with Status("Decompressing...") as status:
        data = decompress_pickle("../data/update_foi_requests.pbz2")

    df = pd.DataFrame(data)

    df.sort_values(by="last_message", ascending=False, inplace=True) # temporary sorting for testing
    
    # Keeping first because we want the most recently updated foi requests (df is sorted by last message)
    df.drop_duplicates(subset="id", inplace=True, keep="first")

    # Removing columns we dont need and setting order (has to be the same as column order in sql table to simplify data import)
    # df = df[["id", "jurisdiction", "refusal_reason", "costs", "due_date", "resolved_on", "first_message", "last_message", "status", "resolution", "user", "public_body"]]

    # extracting public body ID to new column and dropping public body column 
    df["public_body_id"] = df["public_body"].apply(lambda dct: int(dct.get("id")) if dct is not None else None)
    # df["public_body_id"].fillna(0)
    # df["public_body_id"].astype(int)
    df.drop(columns=["public_body"], inplace=True)

    #saving as csv
    df.to_csv("../data/update_foi_requests.csv", index=False)
    
def pp_pb():

    with Status("Decompressing...") as status:
        data = decompress_pickle("../data/update_public_bodies.pbz2")

    df = pd.DataFrame(data)
    
    df.sort_values(by="id", ascending=False, inplace=True) # temporary sorting for testing

    # remove duplicates
    df.drop_duplicates(subset="id", inplace=True, keep="first")

    ### Classification ####
    # classification
    classi = df['classification'].to_list()
    # remove duplicates
    classif = []
    [classif.append(x) for x in classi if x not in classif and not None]
    classif.remove(None)

    # convert to df and remove useless columns
    classification=pd.DataFrame.from_dict((classif))
    classification.sort_values(by="id", ascending=True, inplace=True)
    classification=classification.drop(columns=['slug'])

    # categories
    cate = []
    cat = df["categories"].to_list()
    [cate.append(x) for x in cat if x not in cate and x != []]
    flat_cat = [item for sublist in cate for item in sublist]
    category=pd.DataFrame.from_dict((flat_cat))
    category.sort_values(by="id", ascending=True, inplace=True)

    category = category.drop(columns=['slug', 'is_topic'])
    category = category.drop_duplicates()

    # jurisdiction
    juri = df['jurisdiction'].to_list()

    # remove duplicates
    juris = []
    [juris.append(x) for x in juri if x not in juris and not None]
    
    while None in juris:
        # removing None from list using remove method
        juris.remove(None)
    
    #juris.remove(None)

    # convert to df and remove useless columns
    jurisdiction=pd.DataFrame.from_dict((juris))
    jurisdiction=jurisdiction.drop(columns=['slug', 'site_url', 'region', 'resource_uri', 'description'])
    jurisdiction.sort_values(by="id", ascending=True, inplace=True)
    
    #### complete processing of public data
    df["classification"] = df["classification"].apply(lambda pb: pb['id'] if pb is not None else None)
    df["categories"] = df["categories"].apply(lambda pb: pb[0]['id'] if pb else None)
    df["jurisdiction"] = df["jurisdiction"].apply(lambda pb: pb['id'] if pb is not None else None)

    #df = df.astype({"classification": int, "categories": int, "jurisdiction": int})
    df['classification'] = df['classification'].astype('Int64')
    df['jurisdiction'] = df['jurisdiction'].astype('Int64')
    df['categories'] = df['categories'].astype('Int64')

    ### saving as csv
    # public body
    with Status("Saving as csv...") as status:
        df.to_csv("../data/update_public_bodies.csv", index=False)

    # classification
    with Status("Saving as csv...") as status:
        classification.to_csv("../data/update_classifications.csv", index=False)

    # category
    with Status("Saving as csv...") as status:
        category.to_csv("../data/update_categories.csv", index=False)

    # jurisdiction
    with Status("Saving as csv...") as status:
        jurisdiction.to_csv("../data/update_jurisdictions.csv", index=False)

def pp_messages():
    with Status("Decompressing...") as status:
        data = decompress_pickle("../data/update_messages.pbz2")

    df = pd.DataFrame(data)

    df.sort_values(by="timestamp", ascending=False, inplace=True) # temporary sorting for testing

    # keep useful columns
    # df = df[["id", "request", "sent", "is_response", "is_postal", "kind", "sender_public_body", "recipient_public_body", "status", "timestamp"]]

    # strings with id to int
    df["request"] = df["request"].apply(lambda req: int(req.split("/")[-2]))
    df["sender_public_body"] = df["sender_public_body"].apply(lambda pb: int(pb.split("/")[-2]) if pb is not None else None)
    df["recipient_public_body"] = df["recipient_public_body"].apply(lambda pb: int(pb.split("/")[-2]) if pb is not None else None)

    df.drop_duplicates(subset="id", inplace=True, keep="first")

    # saving as csv
    with Status("Saving as csv...") as status:
        df.to_csv("../data/update_messages.csv", index=False)

#console.print("preprocessing foi requests")
#pp_requests()
#console.print("preprocessing public bodies")
#pp_pb()
#console.print("preprocessing messages")
#pp_messages()