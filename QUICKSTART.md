# Live Lake Monitoring System

## Quick Start Commands

### Initial Setup
```powershell
# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Authenticate Google Earth Engine
python src/gee_auth.py
```

### Running Analysis
```powershell
# Quick analysis (last 6 months)
python src/main.py --quick

# Full analysis
python src/main.py

# Custom config
python src/main.py --config config/custom.yaml
```

### Dashboard
```powershell
# Launch interactive dashboard
streamlit run src/dashboard.py
```

### Jupyter Notebook
```powershell
# Start Jupyter
jupyter notebook notebooks/lake_analysis.ipynb
```

## Common Lakes - Pre-configured Coordinates

### Lake Victoria (Africa)
```yaml
bounds: [31.5, -3.0, 35.0, 0.5]
center: [33.0, -1.0]
zoom: 8
```

### Great Salt Lake (USA)
```yaml
bounds: [-113.0, 40.5, -111.8, 41.8]
center: [-112.4, 41.15]
zoom: 9
```

### Lake Chad (Africa)
```yaml
bounds: [13.0, 12.0, 15.5, 14.5]
center: [14.25, 13.25]
zoom: 8
```

### Aral Sea (Central Asia)
```yaml
bounds: [58.0, 43.5, 62.0, 46.5]
center: [60.0, 45.0]
zoom: 8
```

### Lake Urmia (Iran)
```yaml
bounds: [45.0, 37.0, 46.0, 38.0]
center: [45.5, 37.5]
zoom: 9
```

### Caspian Sea
```yaml
bounds: [46.0, 36.0, 54.0, 47.0]
center: [50.0, 41.5]
zoom: 6
```

## Output Files

### Time Series Data
- `outputs/timeseries/lake_timeseries.csv` - Raw time series
- `outputs/timeseries/lake_timeseries_detailed.csv` - With anomalies
- `outputs/timeseries/lake_timeseries_monthly.csv` - Monthly aggregates

### Maps
- `outputs/maps/latest_water_extent.html` - Current water extent
- `outputs/maps/latest_ndwi.html` - NDWI visualization
- `outputs/maps/change_comparison.html` - Change over time

### Reports
- `outputs/reports/summary_report.txt` - Statistical summary
- `outputs/reports/summary_dashboard.png` - Visual dashboard

## Troubleshooting Quick Fixes

### Authentication Issues
```powershell
# Clear credentials and re-authenticate
Remove-Item -Recurse -Force $env:USERPROFILE\.config\earthengine
python src/gee_auth.py
```

### No Images Found
- Increase `cloud_cover_max` to 40 in `config/config.yaml`
- Extend date range
- Verify bounding box coordinates

### Memory Errors
```powershell
# Use quick mode with fewer months
python src/main.py --quick --months 3
```

### Import Errors
```powershell
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## Key Python Commands

### Test GEE Connection
```python
import ee
ee.Initialize()
print("Connected!")
```

### Quick Data Check
```python
from src.data_fetcher import Sentinel2Fetcher
fetcher = Sentinel2Fetcher([31.5, -3.0, 35.0, 0.5], "2024-01-01", "2024-12-31")
collection = fetcher.get_image_collection()
print(f"Images found: {collection.size().getInfo()}")
```

## Support

- 📖 Full Documentation: `README.md`
- 🛠️ Setup Guide: `docs/SETUP_GUIDE.md`
- 💻 Jupyter Notebook: `notebooks/lake_analysis.ipynb`
- 🌐 Dashboard: http://localhost:8501 (after running streamlit)

## Version Information

- **Project**: Live Lake Monitoring v1.0.0
- **Python**: 3.8+
- **Earth Engine API**: Latest
- **Sentinel-2**: Level 2A (Surface Reflectance)
- **Spatial Resolution**: 10m
- **Temporal Resolution**: 5 days
