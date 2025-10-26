# utils.py
from geopy.distance import geodesic
import math

def distance_meters(a, b):
    return geodesic((a[0], a[1]), (b[0], b[1])).meters

def suggest_route(start_loc, end_loc, avoid_zones=None):
    """
    Very simple stub: returns a linear route interpolated by N points.
    In production: use routing APIs (OSRM, GraphHopper, Google Directions) and apply safety weights.
    """
    if not start_loc or not end_loc:
        return []

    lat1, lng1 = start_loc
    lat2, lng2 = end_loc
    points = []
    steps = 6
    for t in range(steps+1):
        frac = t/steps
        lat = lat1 + (lat2 - lat1) * frac
        lng = lng1 + (lng2 - lng1) * frac
        points.append([lat, lng])
    return points

def is_within_zone(point, zone):
    # point = (lat, lng), zone = DangerZone-like dict with lat,lng,radius_m
    return distance_meters(point, (zone["lat"], zone["lng"])) <= zone["radius_m"]
