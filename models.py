# models.py
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Boolean
from sqlalchemy.sql import func
from database import Base

class CommunityPost(Base):
    __tablename__ = "community_posts"
    id = Column(Integer, primary_key=True, index=True)
    user = Column(String(100), default="Anonymous")
    text = Column(Text)
    rating = Column(Integer, default=3)
    lat = Column(Float, nullable=True)
    lng = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class DangerZone(Base):
    __tablename__ = "danger_zones"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150))
    lat = Column(Float)
    lng = Column(Float)
    level = Column(String(20))  # e.g., 'High', 'Medium', 'Low'
    radius_m = Column(Integer, default=200)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Setting(Base):
    __tablename__ = "settings"
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(100), unique=True, index=True)
    value = Column(String(500))

class RouteRequestLog(Base):
    __tablename__ = "route_requests"
    id = Column(Integer, primary_key=True, index=True)
    start = Column(String(200))
    end = Column(String(200))
    safety_score = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
