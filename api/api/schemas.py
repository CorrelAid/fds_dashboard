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
    stats_percentage_costs: float
    stats_success_rate: dict

class GeneralInfo(BaseModel):
    jurisdictions: dict
    public_bodies: dict
  # campaigns: dict
    
class Ranking(BaseModel):
    ranking: List[dict]




    

    