from pydantic import BaseModel
from pydantic.schema import List
from datetime import timedelta


class Stats(BaseModel):
    foi_requests: int
    foi_requests_resolved: int
    foi_requests_not_resolved: int
    users: int
    dist_resolution: List[dict]
    dist_status: List[dict]
    percentage_costs: float
    percentage_withdrawn: float
    max_costs: dict
    avg_costs: float
    overdue_total: int
    overdue_rate: float
    initial_reaction_time: timedelta
    resolved_time: timedelta
    requests_by_month: List[dict]


class GeneralInfo(BaseModel):
    jurisdictions: List[dict]
    public_bodies: List[dict]
    campaigns: List[dict]


class Ranking(BaseModel):
    ranking: List[dict]


class CampaignStarts(BaseModel):
    campaign_starts: List[dict]
