# 🌍 Google Earth Engine Live Lake Monitoring Setup

## Step-by-Step Setup Guide

### Step 1: Verify Your Google Cloud Project
1. Open: https://console.cloud.google.com/
2. Ensure you're signed in as: **rishwanthuk20@gmail.com**
3. Select your project: **lake-monitoring-rishwanth**
4. Copy the **Project ID** (it should be: `lake-monitoring-rishwanth`)

### Step 2: Enable Required APIs
1. Go to: https://console.cloud.google.com/apis/library
2. Search for: **"Earth Engine API"**
3. Click on it and press **"ENABLE"**
4. Wait for it to complete (shows "API enabled" ✓)

### Step 3: Grant Yourself Access
1. Go to: https://console.cloud.google.com/iam-admin/iam
2. Click on **"GRANT ACCESS"** button (top right)
3. Enter email: `rishwanthuk20@gmail.com`
4. Select role: **"Owner"** or **"Editor"**
5. Click **"SAVE"**
6. **Wait 2-3 minutes** for permissions to propagate

### Step 4: Register with Earth Engine
1. Go to: https://earthengine.google.com/signup/
2. Click **"Sign Up"** button
3. Accept the terms
4. You should see: "Congratulations! You are now registered!"

### Step 5: Test Connection
Once setup is complete, run:
```powershell
cd "c:\workspace\water change"
.\venv\Scripts\Activate.ps1
python src/main.py --quick --months 1
```

---

## Expected Output

When successful, you should see:
```
2025-11-02 15:37:45 - INFO - Initializing Google Earth Engine...
2025-11-02 15:37:50 - INFO - ✓ Authenticated with existing credentials
2025-11-02 15:37:51 - INFO - ✓ Connection test successful
2025-11-02 15:37:52 - INFO - ✓ Google Earth Engine initialized successfully

[QUICK ANALYSIS MODE - Last 1 month]
============================================================
STARTING COMPLETE ANALYSIS PIPELINE
============================================================

[STEP 1/7] Fetching Sentinel-2 data...
✓ Found XXX images matching criteria

[STEP 2/7] Processing NDWI for all images...
✓ Processed XXX images

[STEP 3/7] Extracting time series data...
✓ Extracted XXX time points

[STEP 4/7] Performing statistical analysis...
Mean area: XXXX.XX km²

[STEP 5/7] Saving time series data...
✓ Saved time series data

[STEP 6/7] Creating visualizations...
✓ Interactive map saved to: outputs\maps\latest_water_extent.html
✓ NDWI map saved to: outputs\maps\latest_ndwi.html
✓ Comparison map saved to: outputs\maps\change_comparison.html

[STEP 7/7] Generating summary report...
✓ ANALYSIS PIPELINE COMPLETED SUCCESSFULLY

🎉 Analysis completed successfully!
```

---

## Troubleshooting

### Error: "Caller does not have required permission"
- **Solution**: Grant yourself access to the project (Step 3 above)
- Wait 2-3 minutes and try again

### Error: "Earth Engine API is not enabled"
- **Solution**: Enable the API (Step 2 above)

### Error: "no project found"
- **Solution**: Ensure `GEE_PROJECT_ID=lake-monitoring-rishwanth` in `.env`

### Error: "You are not registered"
- **Solution**: Sign up at https://earthengine.google.com/signup/

---

## Output Files

After successful run, outputs will be in:
```
outputs/
├── maps/
│   ├── latest_water_extent.html      ← Interactive map
│   ├── latest_ndwi.html              ← NDWI visualization
│   └── change_comparison.html        ← Change detection
├── timeseries/
│   ├── lake_timeseries.csv           ← Daily data
│   ├── lake_timeseries_monthly.csv   ← Monthly aggregates
│   ├── timeseries_interactive.html   ← Interactive chart
│   ├── timeseries_plot.png           ← Static chart
│   └── seasonal_analysis.png         ← Seasonal patterns
└── reports/
    ├── summary_report.txt            ← Analysis summary
    └── summary_dashboard.png         ← Dashboard chart
```

---

## Next Steps

After successful setup:

1. **View Live Maps**:
   ```powershell
   Start-Process "outputs\maps\latest_water_extent.html"
   ```

2. **Launch Interactive Dashboard**:
   ```powershell
   streamlit run src/dashboard.py
   ```

3. **Set Up Automated Monitoring**:
   ```powershell
   python src/scheduler.py
   ```

---

## Support

For issues with Google Earth Engine:
- Docs: https://developers.google.com/earth-engine
- Support: https://earthengine.google.com/support/
- Community: https://groups.google.com/forum/#!forum/google-earth-engine-developers
