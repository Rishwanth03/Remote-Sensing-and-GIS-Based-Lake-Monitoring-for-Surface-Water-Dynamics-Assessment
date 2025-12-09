troubleshooting
# 🚨 GEE Permission Error - Quick Fix

## Current Status
✅ Configuration is correct
✅ Python packages installed  
❌ Permission issue: Need to grant access to your Gmail account

## Current Setup
- **Gmail Account**: rishwanthuk20@gmail.com
- **Project ID**: lake-monitoring-rishwanth
- **Status**: Permission Denied (403)

---

## ⚡ Quick Fix (2 minutes)

### Step 1: Go to IAM Console
**URL**: https://console.cloud.google.com/iam-admin/iam?project=lake-monitoring-rishwanth

### Step 2: Grant Access
1. Click **"GRANT ACCESS"** button (top right)
2. Enter email: `rishwanthuk20@gmail.com`
3. Select role: **"Owner"** (most permissive)
4. Click **"SAVE"**

### Step 3: Wait & Try Again
- Wait 2-3 minutes for permissions to propagate
- Then run:
```powershell
cd "c:\workspace\water change"
.\venv\Scripts\Activate.ps1
python check_gee_setup.py
```

---

## 🔍 Verification Checklist

Before running the live monitoring, verify:

- [ ] Email address is correct: `rishwanthuk20@gmail.com`
- [ ] Project ID is correct: `lake-monitoring-rishwanth`
- [ ] You're signed in to Google Cloud with that email
- [ ] You can access: https://console.cloud.google.com/
- [ ] You can see the project: lake-monitoring-rishwanth
- [ ] You have "Owner" or "Editor" role on the project
- [ ] 2-3 minutes have passed since granting access

---

## 🎯 Once Permissions are Fixed

Run live monitoring:
```powershell
cd "c:\workspace\water change"
.\venv\Scripts\Activate.ps1
python src/main.py --quick --months 1
```

Expected output:
```
✓ Authenticated with existing credentials
✓ Connection test successful
✓ Google Earth Engine initialized successfully

[STEP 1/7] Fetching Sentinel-2 data...
✓ Found XXX images matching criteria

[STEP 2/7] Processing NDWI for all images...
✓ Processed XXX images

... (continues through all 7 steps)

✅ ANALYSIS PIPELINE COMPLETED SUCCESSFULLY
```

---

## 📂 Output Files After Success

```
outputs/
├── maps/                           (Interactive geospatial maps)
│   ├── latest_water_extent.html   
│   ├── latest_ndwi.html           
│   └── change_comparison.html     
├── timeseries/                     (Time series data & charts)
│   ├── lake_timeseries.csv        
│   ├── lake_timeseries_monthly.csv
│   ├── timeseries_interactive.html
│   ├── timeseries_plot.png
│   └── seasonal_analysis.png
└── reports/                        (Summary reports)
    ├── summary_report.txt
    └── summary_dashboard.png
```

---

## 🌐 View Your Results

### Interactive Maps (Open in Browser)
```
outputs/maps/latest_water_extent.html
outputs/maps/latest_ndwi.html
outputs/maps/change_comparison.html
```

### Dashboard
```powershell
streamlit run src/dashboard.py
# Then open: http://localhost:8501
```

### Data Files
```
outputs/timeseries/lake_timeseries.csv          (Excel/Google Sheets)
outputs/reports/summary_report.txt              (Text editor)
```

---

## 🚀 Command Reference

```powershell
# Activate environment
cd c:\workspace\water change
.\venv\Scripts\Activate.ps1

# Check setup
python check_gee_setup.py

# Run live monitoring (1 month)
python src/main.py --quick --months 1

# Run live monitoring (6 months)
python src/main.py --quick --months 6

# Full analysis (5 years)
python src/main.py

# View dashboard
streamlit run src/dashboard.py

# Automated daily monitoring
python src/scheduler.py
```

---

## 💡 What is Happening?

Your **Live Lake Monitoring System** is:

1. **Fetching** daily Sentinel-2 satellite images from Google Earth Engine
2. **Processing** water indices (NDWI) to detect water extent
3. **Analyzing** temporal patterns (trends, seasonality, anomalies)
4. **Visualizing** results as:
   - Interactive geospatial maps (geemap + Folium)
   - Time series charts (Plotly)
   - Statistical dashboards (Streamlit)
5. **Exporting** data as CSV, HTML, PNG for further analysis

---

## ❓ FAQ

**Q: Why permission error?**
A: Your Gmail account was just added to the project. Google Cloud takes 1-3 minutes to propagate permissions.

**Q: How often does it update?**
A: Sentinel-2 provides new images every 5 days. You can run monitoring daily to check for new data.

**Q: Can I monitor a different lake?**
A: Yes! Edit `config/config.yaml` and update the coordinates.

**Q: How much data is downloaded?**
A: Only indices are calculated (not raw images). Minimal bandwidth usage.

**Q: Is this real-time?**
A: Sentinel-2 has 5-day revisit time. Not true real-time, but near real-time monitoring.

---

## 📞 Support

- **GEE Docs**: https://developers.google.com/earth-engine
- **Setup Help**: https://earthengine.google.com/signup/
- **Community**: https://groups.google.com/forum/#!forum/google-earth-engine-developers

---

**Next**: Grant access to your Gmail account at the IAM console link above, then run `python check_gee_setup.py` again!
