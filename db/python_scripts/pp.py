import pandas as pd
from rich.console import Console
from rich.status import Status
from helpers import decompress_pickle, compressed_pickle

console = Console()


def pp_requests():
    with Status("Decompressing...") as status:
        data = decompress_pickle("data/foi_requests.pbz2")
    
    ###### FOI Requests Table #######

    df = pd.DataFrame(data)

    # Keeping first because we want the most recently updated foi requests (df is sorted by last message)
    df.drop_duplicates(subset="id", inplace=True, keep="first")

    # extracting public body ID to new column 
    df["public_body_id"] = df["public_body"].apply(lambda dct: int(dct.get("id")) if dct is not None else pd.NA)
    
    # string na
    df.loc[df.refusal_reason=="n/a", "refusal_reason"] = pd.NA

    # converting user column to int 
    df['user'] = df['user'].astype('float').astype(pd.Int64Dtype())

    # keeping only required columns
    df = df[["id", "jurisdiction", "refusal_reason", "costs", "due_date",
         "created_at", "last_message", "status", "resolution", "user", "public_body_id", "campaign"]]
    
    
    
    # renaming columns
    df.rename(columns={"jurisdiction": "jurisdiction_id"}, errors="raise", inplace=True)
    df.rename(columns={"campaign": "campaign_id"}, errors="raise", inplace=True)

    # extracting ids from string
    df["jurisdiction_id"] = df["jurisdiction_id"].apply(lambda x: int(x.split("/")[-2]) if x is not None else pd.NA)
    df["campaign_id"] = df["campaign_id"].apply(lambda x: int(x.split("/")[-2]) if x is not None else pd.NA)

    # temporarily 
    df.loc[df.campaign_id==6, "campaign_id"] = pd.NA
    df.loc[df.campaign_id==18, "campaign_id"] = pd.NA
    df.loc[df.campaign_id==19, "campaign_id"] = pd.NA
    df.loc[df.campaign_id==8, "campaign_id"] = pd.NA
    df.loc[df.campaign_id==7, "campaign_id"] = pd.NA




    # making sure df only contains integer NAs
    df = df.fillna(pd.NA)

    id_lst = list(df['id'].unique())
    
    # saving as csv
    df.to_csv("../postgres/data/foi_requests.csv", index=False)

    ###### Public Bodies Table #######

    df = pd.DataFrame(data)

    pb_lst_ = df['public_body'].to_list()

    pb_lst = []
    [pb_lst.append(x) for x in pb_lst_ if x not in pb_lst and not None and pd.notnull(x)]

    df = pd.DataFrame.from_dict(pb_lst)
    df = df[["id","name","jurisdiction"]]

    # rename columnd and extract id from string
    df["jurisdiction"] = df["jurisdiction"].apply(lambda x: int(x.split("/")[-2]) if x is not None else pd.NA)
    df.rename(columns={"jurisdiction": "jurisdiction_id"}, inplace=True)

    # some know cases where pb has no juri !!NDR is assigned hamburg!!
    df.loc[df.id==49901, "jurisdiction_id"] = 6
    df.loc[df.id==49254, "jurisdiction_id"] = 5

    df.to_csv("../postgres/data/public_bodies.csv", index=False)

    return id_lst




def pp_pb():

    with Status("Decompressing...") as status:
        data = decompress_pickle("data/public_bodies.pbz2")

    df = pd.DataFrame(data)

    # remove duplicates
    # df.drop_duplicates(subset="id", inplace=True, keep="first")

    # # some pbs dont have juris
    # df.loc[df.id == 49901, "jurisdiction"] = [{"id": 6}]
    # df.loc[df.id == 49254, "jurisdiction"] = [{"id": 5}]

    # extract juris id
    # df["jurisdiction_id"] = df["jurisdiction"].apply(
    #     lambda dct: int(dct.get("id")) if dct is not None else None)

    # ### Classification ####
    # # classification
    # classi = df['classification'].to_list()
    # # remove duplicates
    # classif = []
    # [classif.append(x) for x in classi if x not in classif and not None]
    # classif.remove(None)

    # # convert to df and remove useless columns
    # classification=pd.DataFrame.from_dict((classif))
    # classification.sort_values(by="id", ascending=True, inplace=True)
    # classification=classification.drop(columns=['slug'])

    # # categories
    # cate = []
    # cat = df["categories"].to_list()
    # [cate.append(x) for x in cat if x not in cate and x != []]
    # flat_cat = [item for sublist in cate for item in sublist]
    # category=pd.DataFrame.from_dict((flat_cat))
    # category.sort_values(by="id", ascending=True, inplace=True)

    # category = category.drop(columns=['slug', 'is_topic'])
    # category = category.drop_duplicates()

    # jurisdictions
    juris_ = df['jurisdiction'].to_list()
    juris = []
    [juris.append(x) for x in juris_ if x not in juris and not None and pd.notnull(x)]

    jurisdiction=pd.DataFrame.from_dict(juris)
    jurisdiction.drop(columns=['slug', 'site_url', 'region', 'resource_uri', 'description',"rank"], inplace=True)
    jurisdiction.dropna(inplace=True)
    
    # complete processing of public data
    # df["classification"] = df["classification"].apply(lambda pb: pb['id'] if pb is not None else None)
    # df["categories"] = df["categories"].apply(lambda pb: pb[0]['id'] if pb else None)
    # df["jurisdiction"] = df["jurisdiction"].apply(lambda pb: pb['id'] if pb is not None else None)

    # df = df.astype({"classification": int, "categories": int, "jurisdiction": int})
    # df['classification'] = df['classification'].astype('Int64')
    # df['jurisdiction'] = df['jurisdiction'].astype('Int64')
    # df['categories'] = df['categories'].astype('Int64')

    # keeping only some cols of pb_df
    # df = df[["id", "name", "jurisdiction_id"]]
    # saving as csv
    # public body
    # with Status("Saving as csv...") as status:
    #     df.to_csv("../postgres/data/public_bodies.csv", index=False)
    

    # # classification
    # with Status("Saving as csv...") as status:
    #     classification.to_csv("../postgres/data/classifications.csv", index=False)

    # # category
    # with Status("Saving as csv...") as status:
    #     category.to_csv("../postgres/data/categories.csv", index=False)

    with Status("Saving as csv...") as status:
        jurisdiction.to_csv("../postgres/data/jurisdictions.csv", index=False)

def pp_messages(id_lst):
    with Status("Decompressing...") as status:
        data = decompress_pickle("data/messages.pbz2")

    df = pd.DataFrame(data)

    df["request"] = df["request"].apply(lambda req: int(req.split("/")[-2]))
    df["sender_public_body"] = df["sender_public_body"].apply(lambda pb: int(pb.split("/")[-2]) if pb is not None else pd.NA)
    df["recipient_public_body"] = df["recipient_public_body"].apply(lambda pb: int(pb.split("/")[-2]) if pb is not None else pd.NA)
    df.drop_duplicates(subset="id", inplace=True, keep="first")

    df.rename(columns={"request": "foi_request_id"}, errors="raise", inplace=True)
    
    df = df.query(f'foi_request_id in {id_lst}')

    # saving as csv
    with Status("Saving as csv...") as status:
        df.to_csv("../postgres/data/messages.csv", index=False)

def pp_campaigns():
    with Status("Decompressing...") as status:
        data_cmp = decompress_pickle("data/campaigns.pbz2")
    df_cmp = pd.DataFrame(data_cmp)
    df_cmp = df_cmp[["id","name","slug","start_date","active"]]
     # saving as csv
    with Status("Saving as csv...") as status:
        df_cmp.to_csv("../postgres/data/campaigns.csv", index=False)

console.print("preprocessing foi requests")
id_lst = pp_requests()
console.print("preprocessing public bodies")
pp_pb()
console.print("preprocessing messages")
pp_messages(id_lst)
pp_campaigns()