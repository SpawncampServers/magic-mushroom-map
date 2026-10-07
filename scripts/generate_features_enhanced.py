#!/usr/bin/env python3
"""Enhanced features with terrain approximations."""
import os
import pandas as pd
import numpy as np

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
PROC_DIR = os.path.join(DATA_DIR, 'processed')
FEAT_DIR = os.path.join(DATA_DIR, 'features')
os.makedirs(FEAT_DIR, exist_ok=True)

def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = np.radians(lat2-lat1); dlon = np.radians(lon2-lon1)
    a = np.sin(dlat/2)**2 + np.cos(np.radians(lat1))*np.cos(np.radians(lat2))*np.sin(dlon/2)**2
    c = 2*np.arctan2(np.sqrt(a), np.sqrt(1-a))
    return R*c

def generate_training():
    pres = pd.read_csv(os.path.join(PROC_DIR, 'occurrences_clean.csv'))
    pres = pres[pres['month'].isin([8,9,10,11])]
    np.random.seed(42)
    n_abs = min(len(pres)*3, 6000)
    lats = np.random.uniform(49.5, 60.5, n_abs)
    lons = np.random.uniform(-11, 3.5, n_abs)
    abs_df = pd.DataFrame({'lat': lats, 'lon': lons, 'presence': 0})
    pres['presence'] = 1
    pres_sub = pres[['lat','lon','presence']].copy()
    data = pd.concat([pres_sub, abs_df], ignore_index=True)
    # Distance to coast approximation (simple)
    coast_lat, coast_lon = 54.0, -5.0  # rough reference
    data['dist_coast_km'] = haversine_km(data['lat'], data['lon'], coast_lat, coast_lon)
    # Elevation rough proxy (not accurate but signal)
    data['lat_norm'] = (data['lat'] - 54.5)
    data['elev_proxy'] = -data['lat_norm']*30 + np.random.randn(len(data))*20  # crude
    data['elev_proxy'] = np.clip(data['elev_proxy'], -50, 800)
    data.to_csv(os.path.join(FEAT_DIR, 'training_enhanced.csv'), index=False)
    print(f'Training: {len(pres_sub)} pres + {len(abs_df)} abs')

if __name__ == '__main__':
    generate_training()