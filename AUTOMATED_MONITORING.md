# 🚀 Automated Lake Monitoring Setup Guide

## 📋 Overview

This guide walks you through setting up automated daily and weekly lake monitoring with email alerts and database persistence.

---

## ⚙️ Configuration

### 1. Update `.env` File

Add these variables to `c:\workspace\water change\.env`:

```bash
# Google Earth Engine
GEE_PROJECT_ID=sage-mind-476714-a4

# Email Alerts (Gmail Example)
ALERT_EMAIL_FROM=your-email@gmail.com
ALERT_EMAIL_PASSWORD=your-app-password  # Use App Password, not regular password
ALERT_EMAIL_TO=recipient1@example.com,recipient2@example.com
ALERT_SMTP_SERVER=smtp.gmail.com
ALERT_SMTP_PORT=587

# Database (optional)
DATABASE_TYPE=sqlite  # or 'postgresql'
DATABASE_PATH=outputs/lake_monitoring.db
```

### 2. Gmail Setup (for email alerts)

To use Gmail for alerts:

1. Enable 2-Factor Authentication on your Google Account
2. Generate an App Password:
   - Go to: https://myaccount.google.com/apppasswords
   - Select "Mail" and "Windows Computer"
   - Copy the 16-character password
   - Paste into `ALERT_EMAIL_PASSWORD` in `.env`

---

## 🎯 Usage

### Option A: Start Automatic Scheduler

**Start daily monitoring at 8:00 AM, weekly at Monday 6:00 AM:**

```powershell
cd c:\workspace\water change
.\venv\Scripts\Activate.ps1
python src/scheduler.py --start
```

**Custom schedule:**

```powershell
python src/scheduler.py --start --daily-time 06:00 --weekly-day tuesday --weekly-time 09:00
```

### Option B: Run Once (Test Mode)

**Test daily monitoring:**

```powershell
python src/scheduler.py --run-once daily
```

**Test weekly monitoring:**

```powershell
python src/scheduler.py --run-once weekly
```

### Option C: Check Status

**View last monitoring run status:**

```powershell
python src/scheduler.py --status
```

---

## 🤖 Windows Task Scheduler Setup

**For continuous automated monitoring**, create a Windows Task:

```powershell
# Create task that starts scheduler at system boot
$Principal = New-ScheduledTaskPrincipal -UserID "NT AUTHORITY\SYSTEM" -RunLevel Highest
$Trigger = New-ScheduledTaskTrigger -AtStartup
$Action = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-NoProfile -WindowStyle Hidden -Command `"cd 'c:\workspace\water change'; .\venv\Scripts\Activate.ps1; python src\scheduler.py --start`""
Register-ScheduledTask -TaskName "LakeMonitoringScheduler" -Principal $Principal -Trigger $Trigger -Action $Action -Force

# Verify
Get-ScheduledTask -TaskName "LakeMonitoringScheduler"
```

---

## 📊 Output Files

### Generated During Monitoring

```
outputs/
├── timeseries/
│   ├── lake_timeseries.csv              # Daily observations
│   ├── lake_timeseries_monthly.csv      # Monthly aggregates
│   └── timeseries_interactive.html      # Interactive chart
├── maps/
│   ├── latest_water_extent.html         # Current extent map
│   ├── latest_ndwi.html                 # NDWI visualization
│   └── change_comparison.html           # Change map
├── reports/
│   ├── summary_dashboard.png            # Summary image
│   └── summary_report.txt               # Text report
├── scheduler.log                         # Scheduler activity
├── lake_monitoring.log                   # Pipeline logs
├── monitoring_history.json               # Historical runs
└── lake_monitoring.db                    # SQLite database (optional)
```

---

## 🔔 Email Alerts

Alerts are sent when:

✅ **Anomalies Detected**: Unusual water area values  
✅ **Monitoring Complete**: Daily/weekly run finished  
❌ **Errors Occur**: Pipeline failures  

### Email Content

Each alert includes:
- Water area measurements
- Statistical deviation from normal
- Timestamp and lake name
- Links to view full reports

---

## 📁 Database Storage

### SQLite (Default)

Automatically creates and updates `lake_monitoring.db` with:

```sql
-- Time series data
CREATE TABLE timeseries (
    date TIMESTAMP UNIQUE,
    area_km2 REAL,
    ndwi_mean REAL,
    is_anomaly BOOLEAN,
    ...
);

-- Monitoring run history
CREATE TABLE monitoring_runs (
    run_date TIMESTAMP,
    analysis_type TEXT,
    status TEXT,
    anomalies_detected INTEGER,
    ...
);

-- Alert log
CREATE TABLE alerts (
    alert_date TIMESTAMP,
    alert_type TEXT,
    anomaly_count INTEGER,
    ...
);
```

### Query Examples

```python
import sqlite3
import pandas as pd

conn = sqlite3.connect('outputs/lake_monitoring.db')

# Get all anomalies
anomalies = pd.read_sql_query(
    "SELECT * FROM timeseries WHERE is_anomaly = 1",
    conn
)

# Get monitoring run history
runs = pd.read_sql_query(
    "SELECT * FROM monitoring_runs ORDER BY run_date DESC LIMIT 10",
    conn
)

# Get statistics
stats = pd.read_sql_query(
    "SELECT COUNT(*), AVG(area_km2), MAX(area_km2) FROM timeseries",
    conn
)
```

---

## 🔍 Monitoring Dashboard

View real-time results in Streamlit:

```powershell
streamlit run src/dashboard.py
```

Access at: http://localhost:8501

---

## 📈 Scheduler Features

### Daily Monitoring (Default: 8:00 AM)
- Analyzes last **1 month** of data
- Fast execution (~2 minutes)
- Detects recent anomalies
- Sends email if issues found

### Weekly Detailed Monitoring (Default: Monday 6:00 AM)
- Analyzes last **3 months** of data
- Comprehensive analysis (~5 minutes)
- Generates full reports
- Updates database

---

## 🛠️ Troubleshooting

### Email alerts not working?

```powershell
# Test email configuration
python src/email_alerter.py
```

Should output:
```
✓ Email alerter is configured and ready
```

If not, check `.env` file for:
- `ALERT_EMAIL_FROM` (sender email)
- `ALERT_EMAIL_PASSWORD` (app password, not regular password)
- `ALERT_EMAIL_TO` (recipient emails)

### Database issues?

```powershell
# Check database integrity
python -c "
import sqlite3
conn = sqlite3.connect('outputs/lake_monitoring.db')
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM timeseries')
print(f'Records: {cursor.fetchone()[0]}')
conn.close()
"
```

### Scheduler not starting?

Check logs:
```powershell
Get-Content outputs/scheduler.log -Tail 50
```

---

## 📊 Monitoring Metrics

The system tracks:

| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| Water Area | Lake surface in km² | > 2.0 σ from mean |
| NDWI | Normalized water index | Calculated automatically |
| Cloud Cover | Image cloud percentage | Max 20% |
| Trend | Rate of area change | Significant change detected |
| Seasonality | Monthly/seasonal patterns | Detected automatically |

---

## 🔄 Data Flow

```
GEE Sentinel-2 Images
         ↓
NDWI Processing
         ↓
Area Calculation
         ↓
Anomaly Detection
         ↓
    Database Export ──→ SQLite / PostgreSQL
         ↓
   Email Alerts (if anomalies)
         ↓
Visualization & Reports
```

---

## 🚦 Next Steps

1. **Configure email**: Update `.env` with Gmail credentials
2. **Start scheduler**: `python src/scheduler.py --start`
3. **Monitor logs**: `Get-Content outputs/scheduler.log -Follow`
4. **View results**: Open `outputs/maps/*.html` in browser
5. **Check database**: Query `lake_monitoring.db` for historical data

---

## 📞 Support

For issues, check:
- `outputs/scheduler.log` - Scheduler activity
- `outputs/lake_monitoring.log` - Pipeline logs
- `outputs/monitoring_history.json` - Run history

---

**Happy Monitoring! 🌊📊**
