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
    asleep_number: int
    asleep_percentage_total: float
    asleep_percentage_not_resolved: float
    overdue_not_resolved: int
    overdue_percentage_not_resolved: float
    percentage_costs: float
    percentage_withdrawn: float
    max_costs: dict
    avg_costs: float
    overdue_total: int
    overdue_rate: float
    initial_reaction_time: timedelta
    resolved_time: timedelta
    refusal_reasons_specified: float
    no_law_applicable: float
    other_or_no_reason: float
    refusal_reasons: List[dict]
    requests_by_month: List[dict]


class GeneralInfo(BaseModel):
    jurisdictions: List[dict]
    public_bodies: List[dict]
    campaigns: List[dict]


class Ranking(BaseModel):
    ranking: List[dict]


class CampaignStarts(BaseModel):
    campaign_starts: List[dict]
