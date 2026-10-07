#!/usr/bin/env python3
"""Export predictions as PMTiles (placeholder - creates sample)."""
import os
import json

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
PRED_DIR = os.path.join(DATA_DIR, 'predictions')
WEB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'web')

os.makedirs(PRED_DIR, exist_ok=True)
os.makedirs(WEB_DIR, exist_ok=True)

# For now, just note - pmtiles needs geospatial processing
# Create simple GeoJSON as fallback
if __name__ == '__main__':
    print('PMTiles export placeholder - would require rasterization')
    # Create GeoJSON from CSV
    import pandas as pd
    csv = os.path.join(PRED_DIR, 'predictions_today.csv')
    if os.path.exists(csv):
        df = pd.read_csv(csv)
        features = []
        for _, row in df.iterrows():
            features.append({
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [float(row['lon']), float(row['lat'])]
                },
                'properties': {'score': float(row['score'])}
            })
        geojson = {'type': 'FeatureCollection', 'features': features}
        out = os.path.join(WEB_DIR, 'predictions.geojson')
        with open(out, 'w') as f:
            json.dump(geojson, f)
        print(f'Saved {out}')