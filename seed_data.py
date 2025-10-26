# seed_data.py
from database import SessionLocal, init_db
from models import DangerZone, CommunityPost
import json

def seed():
    init_db()
    db = SessionLocal()
    # Only seed if empty
    if db.query(DangerZone).count() == 0:
        zones = [
            {"name": "Bliss Highway", "lat": 13.075, "lng": 80.265, "level":"High", "radius_m":250},
            {"name": "Old Market", "lat": 13.065, "lng": 80.26, "level":"Medium", "radius_m":200},
            {"name": "Old Bridge", "lat": 13.055, "lng": 80.252, "level":"Low", "radius_m":150},
        ]
        for z in zones:
            db.add(DangerZone(**z))
    if db.query(CommunityPost).count() == 0:
        posts = [
            {"user":"Rakesh","text":"Be careful near Bliss Highway after 8PM, low lighting there.","rating":3, "lat":13.075, "lng":80.265},
            {"user":"Reshma","text":"Safe and well-Cleaned around Tirumala!","rating":5, "lat":13.085, "lng":80.275}
        ]
        for p in posts:
            db.add(CommunityPost(**p))
    db.commit()
    db.close()
    print("Seed completed.")

if __name__ == "__main__":
    seed()
