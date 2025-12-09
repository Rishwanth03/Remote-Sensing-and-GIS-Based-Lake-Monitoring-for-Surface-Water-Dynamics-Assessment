"""
Google Earth Engine Setup Checker
Verifies GEE configuration and tests connection
"""

import os
import sys
from pathlib import Path
import logging

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def check_environment():
    """Check environment configuration"""
    print("\n" + "="*70)
    print("🌍 GOOGLE EARTH ENGINE SETUP CHECKER")
    print("="*70)
    
    # Check .env file
    print("\n1. Checking .env configuration...")
    env_path = Path('.env')
    if env_path.exists():
        with open(env_path) as f:
            content = f.read()
            if 'GEE_PROJECT_ID' in content:
                # Extract project ID
                for line in content.split('\n'):
                    if line.startswith('GEE_PROJECT_ID='):
                        project_id = line.split('=')[1].strip()
                        print(f"   ✓ Project ID found: {project_id}")
                        break
            else:
                print("   ✗ GEE_PROJECT_ID not found in .env")
                return False
    else:
        print("   ✗ .env file not found")
        return False
    
    # Check Python packages
    print("\n2. Checking Python dependencies...")
    try:
        import ee
        print(f"   ✓ earthengine-api: {ee.__version__ if hasattr(ee, '__version__') else 'installed'}")
    except ImportError:
        print("   ✗ earthengine-api not installed")
        return False
    
    try:
        import geemap
        print(f"   ✓ geemap: installed")
    except ImportError:
        print("   ✗ geemap not installed")
        return False
    
    try:
        import geopandas
        print(f"   ✓ geopandas: installed")
    except ImportError:
        print("   ✗ geopandas not installed")
        return False
    
    return True


def test_gee_connection():
    """Test GEE connection"""
    print("\n3. Testing Google Earth Engine connection...")
    
    try:
        import ee
        from dotenv import load_dotenv
        
        # Load environment
        load_dotenv()
        project_id = os.getenv('GEE_PROJECT_ID')
        
        print(f"   Project ID: {project_id}")
        
        # Try to initialize
        try:
            print("   Attempting to initialize...")
            ee.Initialize(project=project_id)
            print("   ✓ Successfully initialized with cached credentials!")
            
            # Test connection
            print("   Testing GEE connection...")
            test_image = ee.Image('COPERNICUS/S2_SR_HARMONIZED/20230101T000000_20230101T235959_T60MWE')
            _ = test_image.bandNames().getInfo()
            print("   ✓ Connection successful! Earth Engine is working.")
            
            return True
            
        except Exception as e:
            error_msg = str(e)
            if 'not registered' in error_msg.lower():
                print(f"   ✗ Not registered with Earth Engine")
                print(f"   → Sign up at: https://earthengine.google.com/signup/")
            elif 'permission' in error_msg.lower():
                print(f"   ✗ Permission denied for project: {project_id}")
                print(f"   → Grant access at: https://console.cloud.google.com/iam-admin/iam/project?project={project_id}")
            elif 'no project found' in error_msg.lower():
                print(f"   ✗ Project not found or authentication required")
                print(f"   → Verify project ID: {project_id}")
            else:
                print(f"   ✗ Error: {error_msg}")
            return False
            
    except Exception as e:
        print(f"   ✗ Unexpected error: {str(e)}")
        return False


def show_next_steps():
    """Show next steps for setup"""
    print("\n" + "="*70)
    print("📋 NEXT STEPS")
    print("="*70)
    
    print("""
1. If you see ✗ errors above, follow the setup guide:
   → Read: SETUP_GEE.md
   → Or visit: https://console.cloud.google.com/

2. After setup is complete, run the live monitoring:
   → python src/main.py --quick --months 1

3. To view results:
   → Interactive maps in: outputs/maps/
   → Dashboard: streamlit run src/dashboard.py

4. For automated daily monitoring:
   → python src/scheduler.py
""")


def main():
    """Main checker"""
    try:
        # Check environment
        if not check_environment():
            print("\n✗ Environment check failed!")
            show_next_steps()
            return False
        
        # Test GEE
        if not test_gee_connection():
            print("\n⚠ GEE connection test failed")
            show_next_steps()
            return False
        
        # Success
        print("\n" + "="*70)
        print("✅ ALL CHECKS PASSED - READY FOR LIVE MONITORING!")
        print("="*70)
        
        print("""
Your system is configured and ready. You can now:

1. Run live lake monitoring:
   cd c:\\workspace\\water change
   .\\venv\\Scripts\\Activate.ps1
   python src/main.py --quick --months 1

2. View interactive maps:
   outputs/maps/latest_water_extent.html
   outputs/maps/latest_ndwi.html

3. Launch dashboard:
   streamlit run src/dashboard.py

4. Set up automated monitoring:
   python src/scheduler.py
""")
        
        return True
        
    except Exception as e:
        logger.error(f"Setup check failed: {str(e)}")
        show_next_steps()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
