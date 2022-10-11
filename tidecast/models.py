from typing import List, Optional
from pydantic import BaseModel


class Tide(BaseModel):
    timestamp: int
    height: float
    time: str
    type: Optional[str]


class TideDay(BaseModel):
    date: str
    sunrise: int
    sunset: int
    tides: List[Tide]


class LowTide(BaseModel):
    height: float
    time: str


class LowDaylightTides(BaseModel):
    date: str
    tides: List[LowTide]
