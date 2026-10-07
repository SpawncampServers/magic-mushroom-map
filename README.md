# Mushroom Prediction Map (Psilocybe semilanceata)
Live prediction of liberty cap fruiting based on weather, land cover, elevation and occurrence data.

## Stack
- Data: GBIF/NBN, Open-Meteo, ERA5 (Copernicus), SoilGrids, UKCEH/CORINE, SRTM
- Model: MaxEnt/XGBoost (presence-only + pseudo-absences)
- Tiles: PMTiles + MapLibre GL JS
- Infra: Static hosting (Cloudflare/Netlify), scheduled daily updates (cron/GHA)

## Quickstart
1. `pip install -r requirements.txt`
2. `python scripts/fetch_occurrences.py` (NBN/GBIF)
3. `python scripts/fetch_weather.py` (Open-Meteo)
4. `python scripts/preprocess.py`
5. `python scripts/train.py`
6. `python scripts/predict_daily.py`
7. `python scripts/export_pmtiles.py`
8. Serve `web/`