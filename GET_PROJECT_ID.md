# How to Get Your Google Earth Engine Project ID

## Option 1: If You Already Have GEE Access

### Step 1: Go to Google Cloud Console
1. Visit: https://console.cloud.google.com/
2. Sign in with your Google account

### Step 2: Find Your Project ID
- Look at the top of the page, near the Google Cloud logo
- You'll see a dropdown with your project name
- Click it to see the **Project ID** (usually different from the project name)
- Example format: `ee-yourname`, `my-gee-project-123456`, etc.

### Step 3: Copy the Project ID
- Copy the **Project ID** (NOT the project name or number)

## Option 2: If You Need to Register for GEE

### Step 1: Sign Up for Earth Engine
1. Visit: https://earthengine.google.com/signup/
2. Fill out the registration form
3. Select "Academia & Research" or your appropriate category
4. Wait for approval email (usually 1-3 days)

### Step 2: Create/Select a Cloud Project
Once approved:
1. Go to: https://console.cloud.google.com/
2. Create a new project or select an existing one
3. Enable Earth Engine API for that project
4. Note your Project ID

## Step 3: Add Project ID to .env File

Once you have your Project ID, I'll add it to the `.env` file for you.

**Please provide your GEE Project ID in one of these formats:**
- `ee-yourname`
- `my-project-id`
- `project-name-123456`

## Quick Test Commands

After adding the Project ID, test the connection:

```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Test GEE authentication
python src\gee_auth.py

# If successful, run quick analysis
python src\main.py --quick
```

## Need Help?

If you don't have GEE access yet:
1. Register at: https://earthengine.google.com/signup/
2. While waiting for approval, you can still explore the code and tests
3. Once approved, come back with your Project ID and I'll configure it

**What's your GEE Project ID?** (Or do you need help registering?)
