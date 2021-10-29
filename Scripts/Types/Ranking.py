
from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime


class Rank(BaseModel):
    team: int
    rank: int
    opr: float
    vopr: float
    auto: float
    control: float
    endgame: float
    cells: float
    bpm: float
    fouls: float
    power: float


class Rankings(BaseModel):
    # Required Team Metrics
    key: str
    rankings: List[Rank]
    updated: datetime =  datetime.utcnow()

