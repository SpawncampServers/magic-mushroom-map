#!/usr/bin/env python3
"""Predict with enhanced model."""
import os
import joblib
import pandas as pd
import numpy as np

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'model')
PRED_DIR = os.path.join(DATA_DIR, 'predictions')
os.makedirs(PRED_DIR, exist_ok=True)

def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = np.radians(lat2-lat1); dlon = np.radians(lon2-lon1)
    a = np.sin(dlat/2)**2 + np.cos(np.radians(lat1))*np.cos(np.radians(lat2))*np.sin(dlon/2)**2
    c = 2*np.arctan2(np.sqrt(a), np.sqrt(1-a))
    return R*c

def predict():
    m = os.path.join(MODEL_DIR, 'model_rf.joblib')
    clf = joblib.load(m)
    lats = np.arange(50, 59.5, 0.15)
    lons = np.arange(-8, 2.5, 0.15)
    res = []
    coast_lat, coast_lon = 54.0, -5.0
    for la in lats:
        for lo in lons:
            d = haversine_km(la,lo,coast_lat,coast_lon)
            e = -((la-54.5))*30 + np.random.randn()*5
            e = np.clip(e,-50,800)
            p = clf.predict_proba([[la,lo,d,e]])[0,1]
            # downweight water-ish areas crudely? reduce if very low elevation coastal flats? simple heuristic
            if e < 5:  # near sea level rough - maybe less typical
                p *= 0.7
            res.append({'lat': float(la), 'lon': float(lo), 'score': float(np.clip(p,0,1))})
    df = pd.DataFrame(res)
    df.to_csv(os.path.join(PRED_DIR, 'predictions_today.csv'), index=False)
    print(f'Saved {len(df)}')

if __name__ == '__main__':
    predict()