# main.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal, init_db
import models, schemas, ml_model, utils
from models import CommunityPost, DangerZone, RouteRequestLog, Setting
from schemas import RouteRequest, SafetyPrediction, CommunityPostCreate, CommunityPostOut, DangerZoneOut
import os

app = FastAPI(title="SafePath AI - Backend")

# Allow CORS for frontend localhost:3000 (React) — adjust in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to frontend origin in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize DB & load model
init_db()
MODEL_PATH = os.getenv("MODEL_PATH", "./model.joblib")
try:
    model = ml_model.load_model(MODEL_PATH)
    print("ML model loaded.")
except Exception as e:
    model = None
    print("ML model not found. Run train_model.py to create one.", e)

@app.get("/health")
def health():
    return {"status":"ok"}

@app.post("/predict_safety", response_model=SafetyPrediction)
def predict_safety(payload: dict):
    """
    Accepts a dict with features: time, crime, traffic, lighting, dist_police.
    Returns safety_score and ai_confidence.
    """
    if model is None:
        raise HTTPException(status_code=500, detail="Model not available. Train model first.")
    out = ml_model.predict_safety_features(model, payload)
    return out

@app.post("/get_safe_route")
def get_safe_route(request: RouteRequest, db: Session = Depends(get_db)):
    """
    Returns:
      - route: list of lat/lng points (simple interpolation stub)
      - safety_score, ai_confidence
      - nearby_danger_zones
    """
    # Simple safeguard: require coordinates to get a route; if not provided, attempt fallback
    start_loc = None
    end_loc = None
    # If front end passed start_loc/end_loc use them
    if request.start_loc:
        start_loc = (request.start_loc.lat, request.start_loc.lng)
    if request.end_loc:
        end_loc = (request.end_loc.lat, request.end_loc.lng)

    if not (start_loc and end_loc):
        raise HTTPException(status_code=400, detail="Provide start_loc and end_loc coordinates (lat,lng).")

    # Get danger zones
    zones = db.query(DangerZone).all()
    zone_list = [{"id":z.id,"name":z.name,"lat":z.lat,"lng":z.lng,"level":z.level,"radius_m":z.radius_m} for z in zones]

    # Get feature estimates for ML: Here we create heuristics — replace with real live data.
    # Example heuristic: crime density = mean of nearby zone severity; traffic: random / external API; lighting: placeholder
    # For demo, we'll compute crime feature as number of High/Medium zones near path
    features = {
        "time": 12,
        "crime": 30,
        "traffic": 40,
        "lighting": 60,
        "dist_police": 500
    }

    if model:
        pred = ml_model.predict_safety_features(model, features)
    else:
        pred = {"safety_score": 70.0, "ai_confidence": 70.0}

    # Route suggestion stub
    route = utils.suggest_route(start_loc, end_loc, avoid_zones=zone_list)

    # Log request
    log = RouteRequestLog(start=request.start, end=request.end, safety_score=pred["safety_score"])
    db.add(log)
    db.commit()

    # Return payload
    return {
        "route": route,
        "safety_score": pred["safety_score"],
        "ai_confidence": pred["ai_confidence"],
        "danger_zones": zone_list
    }

# Community endpoints
@app.post("/community/posts", response_model=CommunityPostOut)
def create_post(payload: CommunityPostCreate, db: Session = Depends(get_db)):
    post = CommunityPost(
        user=payload.user,
        text=payload.text,
        rating=payload.rating,
        lat=payload.lat,
        lng=payload.lng
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@app.get("/community/posts", response_model=list[CommunityPostOut])
def list_posts(db: Session = Depends(get_db)):
    posts = db.query(CommunityPost).order_by(CommunityPost.created_at.desc()).all()
    return posts

# Danger zones
@app.get("/danger_zones", response_model=list[DangerZoneOut])
def danger_zones(db: Session = Depends(get_db)):
    zones = db.query(DangerZone).all()
    return zones

@app.post("/danger_zones")
def create_danger_zone(z: DangerZoneOut, db: Session = Depends(get_db)):
    zone = DangerZone(name=z.name, lat=z.lat, lng=z.lng, level=z.level, radius_m=z.radius_m)
    db.add(zone)
    db.commit()
    db.refresh(zone)
    return {"status":"ok", "id": zone.id}

# Settings
@app.get("/settings")
def get_settings(db: Session = Depends(get_db)):
    rows = db.query(Setting).all()
    return {r.key: r.value for r in rows}

@app.post("/settings")
def set_setting(key: str, value: str, db: Session = Depends(get_db)):
    row = db.query(Setting).filter(Setting.key == key).first()
    if not row:
        row = Setting(key=key, value=value)
        db.add(row)
    else:
        row.value = value
    db.commit()
    return {"status":"ok"}

# Run uvicorn by CLI: uvicorn main:app --reload --port 8000
