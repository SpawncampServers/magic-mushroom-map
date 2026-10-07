#!/usr/bin/env python3
"""Fetch weather data (Open-Meteo) for UK+Ireland grid."""
import os
import json
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
RAW_DIR = os.path.join(DATA_DIR, 'raw')
os.makedirs(RAW_DIR, exist_ok=True)

def fetch_openmeteo_grid():
    """Fetch current forecast for sample grid (to be expanded)."""
    # Simple test fetch
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        'latitude': 54.5,
        'longitude': -3.0,
        'daily': 'temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max,weather_code',
        'hourly': 'temperature_2m,precipitation,soil_moisture_0_to_1cm,relative_humidity_2m,dew_point_2m',
        'forecast_days': 7,
        'timezone': 'auto'
    }
    try:
        r = requests.get(url, params=params, timeout=60)
        r.raise_for_status()
        data = r.json()
        out = os.path.join(RAW_DIR, 'openmeteo_sample.json')
        with open(out, 'w') as f:
            json.dump(data, f, indent=2)
        print(f'Saved sample to {out}')
    except Exception as e:
        print(f'Error: {e}')

if __name__ == '__main__':
    fetch_openmeteo_grid()