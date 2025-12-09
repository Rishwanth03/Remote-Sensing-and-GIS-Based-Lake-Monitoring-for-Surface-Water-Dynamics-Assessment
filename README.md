# 🌊 Live Lake Monitoring Using Remote Sensing and GIS

A comprehensive system for real-time monitoring of lake water surface area changes using Google Earth Engine, Sentinel-2 satellite imagery, and geospatial analysis tools.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Google Earth Engine](https://img.shields.io/badge/Google%20Earth%20Engine-API-green)](https://earthengine.google.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Outputs](#outputs)
- [Dashboard](#dashboard)
- [Extending the System](#extending-the-system)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

---

## 🌍 Overview

This project implements an automated lake monitoring system that:
- Fetches Sentinel-2 satellite imagery via Google Earth Engine API
- Calculates the Normalized Difference Water Index (NDWI)
- Extracts water body surface areas over time
- Analyzes temporal trends, seasonal patterns, and anomalies
- Generates interactive maps and visualizations
- Provides a live dashboard for real-time monitoring

**Use Cases:**
- Environmental monitoring and conservation
- Water resource management
- Drought and flood assessment
- Climate change impact studies
- Academic research and education

---

## ✨ Features

### Core Capabilities
- ✅ **Automated Data Retrieval**: Direct access to Sentinel-2 imagery (10m resolution, 5-day revisit)
- ✅ **Water Detection**: NDWI calculation using McFeeters or Modified NDWI methods
- ✅ **Time Series Analysis**: Extract and analyze lake area changes over time
- ✅ **Statistical Analysis**: Descriptive statistics, trend detection, seasonal patterns
- ✅ **Anomaly Detection**: Identify unusual lake area changes using z-score method
- ✅ **Interactive Visualizations**: Maps, charts, and dashboards
- ✅ **Cloud Masking**: Automatic cloud removal for accurate analysis
- ✅ **Export Capabilities**: CSV data export, HTML maps, PNG plots

### Advanced Features
- 📊 Seasonal decomposition and analysis
- 📈 Linear trend analysis with R² fit quality
- 🗺️ Interactive map generation with geemap
- 📱 Real-time dashboard with Streamlit
- 🔔 Anomaly detection and alerting
- 📄 Automated report generation
- 🔄 Monthly/weekly aggregation options

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   Google Earth Engine                       │
│              Sentinel-2 Satellite Imagery                   │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                  Data Fetcher Module                        │
│     - Filter by date, region, cloud cover                   │
│     - Monthly composites                                    │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                  NDWI Processor Module                      │
│     - Calculate NDWI (Green - NIR)/(Green + NIR)           │
│     - Extract water pixels (threshold > 0)                  │
│     - Calculate surface area                                │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              Time Series Analyzer Module                    │
│     - Statistical analysis                                  │
│     - Trend detection                                       │
│     - Seasonal patterns                                     │
│     - Anomaly detection                                     │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              Visualization & Dashboard                      │
│     - Interactive maps (geemap)                             │
│     - Time series plots (matplotlib, plotly)                │
│     - Live dashboard (Streamlit)                            │
└─────────────────────────────────────────────────────────────┘
```

---

## 💻 Installation

### Prerequisites
- Python 3.8 or higher
- Google Earth Engine account ([Sign up here](https://earthengine.google.com/signup/))
- Internet connection for satellite data access

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd "water change"
```

### Step 2: Create Virtual Environment
```powershell
# Windows PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1

# If you get execution policy error, run:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Step 3: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 4: Configure Environment
```powershell
# Copy example environment file
cp .env.example .env

# Edit .env with your Google Earth Engine project ID
# notepad .env
```

### Step 5: Authenticate Google Earth Engine
```powershell
python src/gee_auth.py
```
This will open a browser window for authentication. Sign in with your Google account.

---

## 🚀 Quick Start

### Run Complete Analysis
```powershell
python src/main.py
```

### Run Quick Analysis (Last 6 Months)
```powershell
python src/main.py --quick --months 6
```

### Launch Interactive Dashboard
```powershell
streamlit run src/dashboard.py
```

### Open Jupyter Notebook
```powershell
jupyter notebook notebooks/lake_analysis.ipynb
```

---

## 📖 Usage

### 1. Configure Your Lake

Edit `config/config.yaml`:

```yaml
lake:
  name: "Your Lake Name"
  bounds: [min_lon, min_lat, max_lon, max_lat]  # Bounding box
  center_lon: 33.0
  center_lat: -1.0
  zoom_level: 8

sentinel:
  start_date: "2020-01-01"
  end_date: "2024-12-31"
  cloud_cover_max: 20  # Maximum cloud coverage %
```

**Finding Coordinates:**
- Use [Google Maps](https://maps.google.com): Right-click → "What's here?"
- Use [Google Earth Engine Code Editor](https://code.earthengine.google.com/)
- Format: [West, South, East, North] or [min_lon, min_lat, max_lon, max_lat]

### 2. Run Analysis

```powershell
# Full analysis
python src/main.py

# Quick analysis
python src/main.py --quick

# Custom config file
python src/main.py --config custom_config.yaml
```

### 3. View Results

**Interactive Maps:**
- Open `outputs/maps/*.html` in your browser

**Time Series Data:**
- CSV files in `outputs/timeseries/`
- Import into Excel, Python, or R for further analysis

**Reports:**
- Text reports in `outputs/reports/`
- Summary statistics and trend analysis

### 4. Launch Dashboard

```powershell
streamlit run src/dashboard.py
```

Access at: http://localhost:8501

---

## 📁 Project Structure

```
water change/
├── config/
│   └── config.yaml              # Main configuration file
├── src/
│   ├── gee_auth.py              # GEE authentication module
│   ├── data_fetcher.py          # Sentinel-2 data retrieval
│   ├── ndwi_processor.py        # NDWI calculation and water extraction
│   ├── timeseries_analysis.py  # Time series analysis
│   ├── visualization.py         # Visualization creation
│   ├── main.py                  # Main processing pipeline
│   └── dashboard.py             # Streamlit dashboard
├── notebooks/
│   └── lake_analysis.ipynb      # Interactive Jupyter notebook
├── data/
│   ├── raw/                     # Raw data (if any)
│   └── processed/               # Processed data
├── outputs/
│   ├── maps/                    # HTML interactive maps
│   ├── timeseries/              # CSV time series data
│   └── reports/                 # Generated reports
├── docs/
│   └── SETUP_GUIDE.md           # Detailed setup instructions
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore file
└── README.md                    # This file
```

---

## ⚙️ Configuration

### Lake Configuration

```yaml
lake:
  name: "Lake Victoria"
  bounds: [31.5, -3.0, 35.0, 0.5]  # [min_lon, min_lat, max_lon, max_lat]
  center_lon: 33.0
  center_lat: -1.0
  zoom_level: 8
```

### NDWI Methods

**McFeeters NDWI (Default):**
```
NDWI = (Green - NIR) / (Green + NIR)
```
- Best for general water body detection
- Uses Sentinel-2 bands B3 (Green) and B8 (NIR)

**Modified NDWI:**
```
MNDWI = (Green - SWIR) / (Green + SWIR)
```
- Better for built-up areas and turbid water
- Uses Sentinel-2 bands B3 (Green) and B11 (SWIR)

### Date Range

```yaml
sentinel:
  start_date: "2020-01-01"
  end_date: "2024-12-31"
```

**Tips:**
- Longer periods: Better trend analysis (3-5 years recommended)
- Shorter periods: Faster processing, recent changes
- Sentinel-2 data available from 2015-06-23 onwards

---

## 📊 Outputs

### 1. Time Series Data (CSV)

**lake_timeseries.csv:**
```csv
date,area_km2
2020-01-05,68234.56
2020-01-15,68156.32
...
```

**lake_timeseries_detailed.csv:**
Includes year, month, season, z_score, is_anomaly

**lake_timeseries_monthly.csv:**
Monthly aggregates with mean, median, std, min, max

### 2. Interactive Maps (HTML)

- **latest_water_extent.html**: Most recent water extent
- **latest_ndwi.html**: NDWI visualization
- **change_comparison.html**: First vs. last comparison

### 3. Visualizations (PNG)

- **timeseries_plot.png**: Line chart of area over time
- **seasonal_analysis.png**: Seasonal patterns
- **summary_dashboard.png**: Comprehensive dashboard

### 4. Reports (TXT)

- **summary_report.txt**: Statistical summary and trends

---

## 📱 Dashboard

The Streamlit dashboard provides:

- **📊 Key Metrics**: Current area, mean, min, max, recent changes
- **📈 Interactive Charts**: Zoomable time series plots
- **📅 Date Filtering**: Select custom date ranges
- **⚠️ Anomaly Alerts**: Highlighted unusual observations
- **💾 Data Export**: Download filtered data as CSV
- **🔄 Auto-refresh**: Real-time updates

**Features:**
- Responsive design
- Mobile-friendly
- Export capabilities
- Custom date ranges
- Seasonal analysis
- Anomaly detection

---

## 🔧 Extending the System

### Add New Water Quality Indices

Edit `src/ndwi_processor.py`:

```python
def calculate_chlorophyll(self, image: ee.Image) -> ee.Image:
    """Calculate chlorophyll-a concentration"""
    blue = image.select('B2')
    green = image.select('B3')
    red = image.select('B4')
    
    # Implement your algorithm
    chlorophyll = ...
    
    return chlorophyll.rename('CHLOROPHYLL')
```

### Monitor Multiple Lakes

Create multiple config files:

```yaml
# config/lake_chad.yaml
lake:
  name: "Lake Chad"
  bounds: [13.0, 12.0, 15.5, 14.5]
  ...
```

Run with:
```powershell
python src/main.py --config config/lake_chad.yaml
```

### Integrate Weather Data

Add to `src/data_fetcher.py`:

```python
def fetch_weather_data(self, date):
    """Fetch weather data from OpenWeatherMap API"""
    # Implement API integration
    pass
```

### Add Email Notifications

Edit `config/config.yaml`:

```yaml
notifications:
  enabled: true
  email: "your-email@example.com"
  threshold_change: 10  # Alert if area changes >10%
```

---

## 🐛 Troubleshooting

### Issue: Authentication Failed

**Solution:**
```powershell
# Re-authenticate
python src/gee_auth.py

# Or use earthengine command
earthengine authenticate
```

### Issue: No Images Found

**Possible causes:**
1. Date range too narrow
2. Cloud cover threshold too strict
3. Incorrect bounding box

**Solutions:**
- Increase date range
- Increase `cloud_cover_max` to 30-40%
- Verify coordinates using Google Earth

### Issue: Memory Error

**Solution:**
```powershell
# Run quick analysis mode
python src/main.py --quick --months 3

# Or reduce date range in config.yaml
```

### Issue: Slow Processing

**Tips:**
- Use monthly composites instead of all images
- Reduce region size
- Use `--quick` mode for testing
- Check internet connection

### Issue: Import Errors

**Solution:**
```powershell
# Reinstall dependencies
pip install -r requirements.txt --upgrade

# Or install individually
pip install earthengine-api geemap pandas matplotlib
```

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Setup

```powershell
# Install development dependencies
pip install -r requirements.txt
pip install pytest black flake8

# Run tests
pytest tests/

# Format code
black src/
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Google Earth Engine**: Cloud-based geospatial processing platform
- **ESA Sentinel-2**: Free and open satellite imagery
- **Geemap**: Interactive mapping with Google Earth Engine
- **Streamlit**: Web application framework for data science

### References

- McFeeters, S.K. (1996). The use of the Normalized Difference Water Index (NDWI) in the delineation of open water features. *International Journal of Remote Sensing*, 17(7), 1425-1432.
- Xu, H. (2006). Modification of normalised difference water index (NDWI) to enhance open water features in remotely sensed imagery. *International Journal of Remote Sensing*, 27(14), 3025-3033.

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-repo/discussions)
- **Email**: your-email@example.com

---

## 🚀 Future Enhancements

- [ ] Multi-lake comparison dashboard
- [ ] Machine learning for water quality prediction
- [ ] Integration with IoT sensor data
- [ ] Real-time alerting system
- [ ] Mobile app development
- [ ] API for external integration
- [ ] Docker containerization
- [ ] Automated reporting schedule

---

**Made with ❤️ for environmental monitoring and water resource management**

*Last Updated: October 2025*
