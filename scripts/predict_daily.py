#!/usr/bin/env python3
"""Predict daily suitability."""
import os
import joblib
import pandas as pd
import numpy as np

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'model')
PRED_DIR = os.path.join(DATA_DIR, 'predictions')
os.makedirs(PRED_DIR, exist_ok=True)

def predict():
    model_path = os.path.join(MODEL_DIR, 'model.joblib')
    if not os.path.exists(model_path):
        raise FileNotFoundError('Train model first')
    clf = joblib.load(model_path)
    # Generate grid
    lats = np.arange(50, 59.5, 0.25)
    lons = np.arange(-8, 2.5, 0.25)
    res = []
    for la in lats:
        for lo in lons:
            p = clf.predict_proba([[la,lo]])[0,1]
            res.append({'lat': float(la), 'lon': float(lo), 'score': float(np.clip(p,0,1))})
    df = pd.DataFrame(res)
    out = os.path.join(PRED_DIR, 'predictions_today.csv')
    df.to_csv(out, index=False)
    print(f'Saved {len(df)} predictions')

if __name__ == '__main__':
    predict()