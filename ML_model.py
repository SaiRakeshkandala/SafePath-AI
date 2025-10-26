# ml_model.py
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.calibration import CalibratedClassifierCV
import joblib
import os

MODEL_PATH = os.getenv("MODEL_PATH", "./model.joblib")

def generate_synthetic_data(n=2000, seed=42):
    # Inputs: time_of_day (0-23), crime_density (0-100), foot_traffic (0-100), lighting_score (0-100), distance_to_police (meters)
    rng = np.random.RandomState(seed)
    time = rng.randint(0, 24, size=n)
    crime = rng.normal(loc=30, scale=15, size=n).clip(0,100)
    traffic = rng.normal(loc=40, scale=25, size=n).clip(0,100)
    lighting = rng.normal(loc=60, scale=20, size=n).clip(0,100)
    dist_police = rng.exponential(scale=1000, size=n)  # mean distance in meters

    # Safety score (0/1 safe-ish). This is synthetic formula — replace with your trained labels on real data.
    score_cont = (100 - crime) * 0.4 + lighting * 0.3 + (100 - dist_police / 20) * 0.2 + (100 - traffic) * 0.1
    label = (score_cont > 50).astype(int)

    df = pd.DataFrame({
        "time": time,
        "crime": crime,
        "traffic": traffic,
        "lighting": lighting,
        "dist_police": dist_police,
        "label": label
    })
    return df

def train_and_save(model_path=MODEL_PATH):
    df = generate_synthetic_data()
    X = df[["time","crime","traffic","lighting","dist_police"]]
    y = df["label"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    clf = RandomForestClassifier(n_estimators=150, random_state=42)
    clf.fit(X_train, y_train)

    # calibrate probabilities for better confidence estimates
    calibrated = CalibratedClassifierCV(clf, method='isotonic', cv=3)
    calibrated.fit(X_train, y_train)

    joblib.dump(calibrated, model_path)
    print(f"Model saved to {model_path}")

def load_model(model_path=MODEL_PATH):
    if not os.path.exists(model_path):
        raise FileNotFoundError("Model not trained. Run `train_model.py` first.")
    return joblib.load(model_path)

def predict_safety_features(model, features: dict):
    """
    features: { time, crime, traffic, lighting, dist_police }
    returns: safety_score (0-100), confidence(0-100)
    """
    X = [[
        features.get("time", 12),
        features.get("crime", 30),
        features.get("traffic", 40),
        features.get("lighting", 60),
        features.get("dist_police", 500)
    ]]
    proba = model.predict_proba(X)[0]  # proba for classes [0,1]
    # safety is probability of label==1 (safe-ish)
    safe_prob = float(proba[1])
    # scale to 0-100
    safety_score = round(safe_prob * 100, 2)
    confidence = round(model.predict_proba(X).max() * 100, 2)
    return {"safety_score": safety_score, "ai_confidence": confidence}
