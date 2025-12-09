"""
Simple test script to validate core functionality of the lake monitoring system.

This script runs basic unit tests on the core modules to ensure they work correctly.
"""

import numpy as np
import matplotlib.pyplot as plt
from image_reader import SatelliteImageReader, create_demo_image
from water_indices import WaterIndexCalculator, calculate_ndwi, calculate_mndwi
from change_detection import ChangeDetector, detect_change
from visualization import LakeVisualizer


def test_image_reader():
    """Test image reader functionality."""
    print("Testing image_reader module...")
    
    # Test synthetic image creation
    reader = create_demo_image(width=256, height=256, lake_radius=50)
    bands = reader.get_all_bands()
    
    assert 'green' in bands, "Green band not found"
    assert 'nir' in bands, "NIR band not found"
    assert 'swir' in bands, "SWIR band not found"
    assert bands['green'].shape == (256, 256), "Incorrect band shape"
    
    # Test band reading from arrays
    reader2 = SatelliteImageReader()
    green = np.random.rand(100, 100)
    nir = np.random.rand(100, 100)
    swir = np.random.rand(100, 100)
    reader2.read_bands_from_array(green, nir, swir)
    
    assert reader2.get_band('green').shape == (100, 100), "Band reading failed"
    
    print("  ✓ Image reader tests passed")


def test_water_indices():
    """Test water index calculations."""
    print("Testing water_indices module...")
    
    # Create test data
    green = np.array([[0.2, 0.3], [0.15, 0.25]])
    nir = np.array([[0.4, 0.5], [0.02, 0.03]])
    swir = np.array([[0.3, 0.4], [0.01, 0.02]])
    
    calculator = WaterIndexCalculator()
    
    # Test NDWI
    ndwi = calculator.calculate_ndwi(green, nir)
    assert ndwi.shape == green.shape, "NDWI shape mismatch"
    assert np.all(ndwi >= -1) and np.all(ndwi <= 1), "NDWI values out of range"
    
    # Test MNDWI
    mndwi = calculator.calculate_mndwi(green, swir)
    assert mndwi.shape == green.shape, "MNDWI shape mismatch"
    assert np.all(mndwi >= -1) and np.all(mndwi <= 1), "MNDWI values out of range"
    
    # Test water mask creation
    water_mask = calculator.threshold_water_mask(ndwi, threshold=0.0)
    assert water_mask.shape == ndwi.shape, "Water mask shape mismatch"
    assert np.all((water_mask == 0) | (water_mask == 1)), "Water mask values invalid"
    
    # Test convenience functions
    ndwi2 = calculate_ndwi(green, nir)
    assert np.array_equal(ndwi, ndwi2), "Convenience function failed"
    
    print("  ✓ Water indices tests passed")


def test_change_detection():
    """Test change detection functionality."""
    print("Testing change_detection module...")
    
    # Create test masks
    mask_t1 = np.array([[1, 1, 0], [1, 1, 0], [0, 0, 0]])
    mask_t2 = np.array([[1, 0, 0], [1, 1, 1], [0, 0, 0]])
    
    detector = ChangeDetector()
    
    # Test change detection
    change_map, stats = detector.detect_water_change(mask_t1, mask_t2)
    assert change_map.shape == mask_t1.shape, "Change map shape mismatch"
    assert 'stable_water_pixels' in stats, "Missing statistics"
    assert 'water_loss_pixels' in stats, "Missing statistics"
    assert 'water_gain_pixels' in stats, "Missing statistics"
    
    # Verify change classes
    assert change_map[0, 0] == 1, "Stable water not detected correctly"
    assert change_map[0, 1] == 2, "Water loss not detected correctly"
    assert change_map[1, 2] == 3, "Water gain not detected correctly"
    
    # Test area calculation
    area_stats = detector.calculate_water_area(mask_t1, pixel_size=30.0)
    assert 'water_pixels' in area_stats, "Missing area statistics"
    assert 'water_area_km2' in area_stats, "Missing area statistics"
    assert area_stats['water_pixels'] == 4, "Incorrect pixel count"
    
    # Test multi-temporal analysis
    masks = [mask_t1, mask_t2]
    results = detector.compare_multiple_dates(masks, dates=['T1', 'T2'])
    assert 'areas' in results, "Missing results"
    assert 'changes' in results, "Missing results"
    assert len(results['areas']) == 2, "Incorrect number of areas"
    
    print("  ✓ Change detection tests passed")


def test_visualization():
    """Test visualization functionality."""
    print("Testing visualization module...")
    
    # Create test data
    water_index = np.random.uniform(-1, 1, (100, 100))
    water_mask = np.random.randint(0, 2, (100, 100))
    change_map = np.random.randint(0, 4, (100, 100))
    
    visualizer = LakeVisualizer(figsize=(8, 6))
    
    # Test water index visualization (don't save)
    try:
        fig = visualizer.visualize_water_index(water_index, title="Test NDWI")
        plt.close(fig)
    except Exception as e:
        raise AssertionError(f"Water index visualization failed: {e}")
    
    # Test water mask visualization
    try:
        fig = visualizer.visualize_water_mask(water_mask, title="Test Mask")
        plt.close(fig)
    except Exception as e:
        raise AssertionError(f"Water mask visualization failed: {e}")
    
    # Test change detection visualization
    try:
        fig = visualizer.visualize_change_detection(change_map, title="Test Change")
        plt.close(fig)
    except Exception as e:
        raise AssertionError(f"Change detection visualization failed: {e}")
    
    print("  ✓ Visualization tests passed")


def run_all_tests():
    """Run all test suites."""
    print("\n" + "="*60)
    print("Running Lake Monitoring System Tests")
    print("="*60 + "\n")
    
    try:
        test_image_reader()
        test_water_indices()
        test_change_detection()
        test_visualization()
        
        print("\n" + "="*60)
        print("All tests passed successfully! ✓")
        print("="*60 + "\n")
        return True
    
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return False
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
