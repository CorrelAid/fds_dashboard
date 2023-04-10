from pydantic import BaseModel
from pydantic.schema import Optional, List
from datetime import datetime, timedelta
from dateutil import relativedelta
from collections import OrderedDict

class Stats(BaseModel):
    foi_requests: int
    foi_requests_resolved: int
    foi_requests_not_resolved: int
    users: int
    dist_resolution: List[dict]
    dist_status: List[dict]
    requests_by_month: List[dict]
    percentage_costs: float
    success_rate: dict

class GeneralInfo(BaseModel):
    jurisdictions: List[dict]
    public_bodies: List[dict]
    campaigns: List[dict]
    
class Ranking(BaseModel):
    ranking: List[dict]

class CampaignStarts(BaseModel):
    campaign_starts: List[dict]

class Reaction(BaseModel):
    initial_reaction_time: timedelta
    resolved_time: timedelta

    

    