#!/usr/bin/env python3
"""Generate pseudo-absences and simple features."""
import os
import pandas as pd
import numpy as np
from sklearn.neighbors import KDTree

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
PROC_DIR = os.path.join(DATA_DIR, 'processed')
FEAT_DIR = os.path.join(DATA_DIR, 'features')
os.makedirs(FEAT_DIR, exist_ok=True)

def generate_training():
    pres = pd.read_csv(os.path.join(PROC_DIR, 'occurrences_clean.csv'))
    # Filter to autumn peak months? (Aug-Nov typical)
    pres = pres[pres['month'].isin([8,9,10,11])]
    
    # Generate pseudo-absences: random background points
    np.random.seed(42)
    n_abs = min(len(pres)*2, 4000)
    # UK+Ireland bounds
    lats = np.random.uniform(50, 59, n_abs)
    lons = np.random.uniform(-8, 2, n_abs)
    abs_df = pd.DataFrame({'lat': lats, 'lon': lons, 'presence': 0})
    pres['presence'] = 1
    # Merge
    pres_sub = pres[['lat','lon','presence']].copy()
    data = pd.concat([pres_sub, abs_df], ignore_index=True)
    # Simple spatial features (placeholder - elevation/cover later)
    data['elev_approx'] = 0  # placeholder
    data.to_csv(os.path.join(FEAT_DIR, 'training.csv'), index=False)
    print(f'Training data: {len(pres_sub)} pres + {len(abs_df)} abs = {len(data)} total')

if __name__ == '__main__':
    generate_training()