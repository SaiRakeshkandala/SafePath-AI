# schemas.py
from pydantic import BaseModel
from typing import Optional, List

class Location(BaseModel):
    lat: float
    lng: float

class RouteRequest(BaseModel):
    start: str
    end: str
    start_loc: Optional[Location] = None
    end_loc: Optional[Location] = None
    avoid_high_risk: Optional[bool] = True

class SafetyPrediction(BaseModel):
    safety_score: float  # 0-100 (higher == safer)
    ai_confidence: float  # 0-100

class CommunityPostCreate(BaseModel):
    user: Optional[str] = "Anonymous"
    text: str
    rating: Optional[int] = 3
    lat: Optional[float] = None
    lng: Optional[float] = None

class CommunityPostOut(BaseModel):
    id: int
    user: str
    text: str
    rating: int
    lat: Optional[float]
    lng: Optional[float]
    created_at: str

    class Config:
        orm_mode = True

class DangerZoneOut(BaseModel):
    id: int
    name: str
    lat: float
    lng: float
    level: str
    radius_m: int

    class Config:
        orm_mode = True
