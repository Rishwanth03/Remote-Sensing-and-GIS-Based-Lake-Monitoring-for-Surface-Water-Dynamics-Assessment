# Google Earth Engine Setup Instructions

## Current Status
✅ Python environment set up
✅ Dependencies installed
✅ GEE authentication completed (token saved)
❌ Need valid GEE Project ID

## Next Steps to Run the Project

### 1. Get Your Google Earth Engine Project ID

**Option A: If you already have GEE access**
1. Go to: https://console.cloud.google.com/
2. Look at the top of the page - your project ID is shown in the project selector
3. It's usually in format like: `ee-yourname` or `your-project-name`

**Option B: If you need to register for GEE**
1. Sign up at: https://earthengine.google.com/signup/
2. Wait for approval (usually 1-3 days)
3. Once approved, create or select a cloud project
4. Note your project ID

### 2. Update the .env File

Edit the file: `.env` (in the project root)

Replace this line:
```
GEE_PROJECT_ID=
```

With your actual project ID:
```
GEE_PROJECT_ID=your-actual-project-id
```

### 3. Run a Quick Test

Once you have the correct project ID in `.env`, run:

```powershell
.\venv\Scripts\Activate.ps1
python src\gee_auth.py
```

You should see: "✓ GEE authentication successful!"

### 4. Run Your First Analysis

**Quick test (6 months of data):**
```powershell
python src\main.py --quick
```

**Full analysis (all data in config.yaml):**
```powershell
python src\main.py
```

### 5. Launch the Dashboard

```powershell
streamlit run src\dashboard.py
```

Then open your browser to: http://localhost:8501

## Troubleshooting

### "PERMISSION_DENIED" Error
- Make sure your GEE_PROJECT_ID is correct
- Verify you have Earth Engine enabled for your project
- Visit: https://console.cloud.google.com/apis/library/earthengine.googleapis.com

### "Project not found" Error
- Double-check your project ID spelling
- Ensure you're using the project ID, not the project name
- The project must have Earth Engine API enabled

### Need Help?
1. Check the full setup guide: `docs/SETUP_GUIDE.md`
2. See quick commands: `docs/QUICKSTART.md`
3. Review the README: `README.md`

## Alternative: Use Jupyter Notebook

If you prefer an interactive approach:

```powershell
.\venv\Scripts\Activate.ps1
jupyter notebook notebooks\lake_analysis.ipynb
```

This provides a step-by-step interactive tutorial.
