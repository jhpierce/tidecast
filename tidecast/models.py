from typing import List, Optional

from pydantic import BaseModel


class Tide(BaseModel):
    """Model for storing tide information, as seen in tide-forecast.com."""
    timestamp: int
    height: float
    time: str
    type: Optional[str]  # Should probably be an Enum


class TideDay(BaseModel):
    """Model for storing a day's worth of tides, as seen in tide-forecast.com."""
    date: str
    sunrise: int
    sunset: int
    tides: List[Tide]


class LowTide(BaseModel):
    """Results model representing a low tide."""
    height: float
    time: str


class LowDaylightTides(BaseModel):
    """Results model representing daylight low tide information."""
    date: str
    tides: List[LowTide]
