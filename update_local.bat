@echo off
cd /d "C:\Users\JLBor\OneDrive\Desktop\Psilocybe semilanceatamap\project"
python scripts/generate_features_enhanced.py
python scripts/train_enhanced.py
python scripts/predict_enhanced_fast.py
python scripts/export_pmtiles.py
echo Done
pause