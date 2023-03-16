from pydantic import BaseModel
from pydantic.schema import Optional, List
from datetime import datetime

class TotalStats(BaseModel):
    total_foi_requests: int
    total_users: int
    total_dist_resolution: dict
    total_dist_status: dict
    total_requests_by_month: dict

class GeneralInfo(BaseModel):
    jurisdictions: dict
    public_bodies: dict
    
class Ranking(BaseModel):
    public_bodies: List[dict]
    jurisdictions: List[dict]
    

    