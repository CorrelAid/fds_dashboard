from pydantic import BaseModel
from pydantic.schema import Optional, List
from datetime import datetime
from collections import OrderedDict

class Stats(BaseModel):
    stats_foi_requests: int
    stats_users: int
    stats_dist_resolution: dict
    stats_dist_status: dict
    stats_requests_by_month: dict

class GeneralInfo(BaseModel):
    jurisdictions: dict
    public_bodies: dict
  #  campaigns: dict
    
class Ranking_public_body(BaseModel):
    public_bodies: List[dict]

class Ranking_jurisdiction(BaseModel):
    jurisdictions: List[dict]
    

    