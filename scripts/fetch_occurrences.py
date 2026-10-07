#!/usr/bin/env python3
"""Fetch Psilocybe semilanceata occurrence records from NBN Atlas/GBIF."""
import os
import json
import requests
import pandas as pd
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
RAW_DIR = os.path.join(DATA_DIR, 'raw')
os.makedirs(RAW_DIR, exist_ok=True)

# NBN Atlas: species ID from text file - NBNSYS0000021551
NBN_TAXON = "NBNSYS0000021551"

def fetch_nbn():
    """Fetch NBN Atlas occurrence records."""
    # NBN Atlas API - occurrences search
    url = "https://records-ws.nbnatlas.org/occurrences/search"
    params = {
        'q': f'lsid:{NBN_TAXON}',
        'fq': 'occurrence_status:present',
        'pageSize': 1000,
        'start': 0
    }
    all_records = []
    while True:
        try:
            r = requests.get(url, params=params, timeout=120)
            r.raise_for_status()
            data = r.json()
            occs = data.get('occurrences', [])
            if not occs:
                break
            all_records.extend(occs)
            print(f'Fetched {len(all_records)} records so far...')
            if len(occs) < params['pageSize']:
                break
            params['start'] += params['pageSize']
        except Exception as e:
            print(f'Error fetching: {e}')
            break
    df = pd.DataFrame(all_records)
    out = os.path.join(RAW_DIR, 'nbn_occurrences.json')
    with open(out, 'w') as f:
        json.dump(all_records, f, indent=2)
    # Also save CSV for easy reading
    out_csv = os.path.join(RAW_DIR, 'nbn_occurrences.csv')
    df.to_csv(out_csv, index=False)
    print(f'Saved {len(df)} records to {out} and {out_csv}')
    return df

if __name__ == '__main__':
    fetch_nbn()