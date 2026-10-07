#!/usr/bin/env python3
"""Preprocess occurrence records for modeling."""
import os
import json
import pandas as pd
import numpy as np

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
RAW_DIR = os.path.join(DATA_DIR, 'raw')
PROC_DIR = os.path.join(DATA_DIR, 'processed')
os.makedirs(PROC_DIR, exist_ok=True)

def preprocess():
    df = pd.read_csv(os.path.join(RAW_DIR, 'nbn_occurrences.csv'))
    
    # Extract key fields
    records = []
    for _, row in df.iterrows():
        try:
            event_date = row.get('eventDate')
            if pd.isna(event_date):
                continue
            # Convert timestamps
            if isinstance(event_date, (int, float)) and event_date > 1e10:
                # milliseconds or seconds
                if event_date > 1e12:
                    dt = pd.to_datetime(event_date, unit='ms', errors='coerce')
                else:
                    dt = pd.to_datetime(event_date, unit='s', errors='coerce')
            else:
                dt = pd.to_datetime(event_date, errors='coerce')
            if pd.isna(dt) or dt.year < 1950 or dt.year > 2030:
                continue
            records.append({
                'lat': row.get('decimalLatitude'),
                'lon': row.get('decimalLongitude'),
                'date': dt.date(),
                'month': dt.month,
                'year': dt.year,
                'uncertainty': row.get('coordinateUncertaintyInMeters', 0)
            })
        except Exception:
            continue
    
    out_df = pd.DataFrame(records)
    out_df = out_df.dropna(subset=['lat', 'lon', 'date'])
    out_df = out_df[out_df['lat'].between(49, 61) & out_df['lon'].between(-11, 3)]
    out_df = out_df[out_df['uncertainty'] < 20000]  # filter very coarse
    
    out_path = os.path.join(PROC_DIR, 'occurrences_clean.csv')
    out_df.to_csv(out_path, index=False)
    print(f'Saved {len(out_df)} cleaned records to {out_path}')

if __name__ == '__main__':
    preprocess()