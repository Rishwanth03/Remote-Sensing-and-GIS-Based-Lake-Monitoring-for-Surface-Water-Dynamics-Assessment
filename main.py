"""
Main script demonstrating the Remote Sensing and GIS-Based Lake Monitoring System.

This script demonstrates:
1. Reading satellite imagery
2. Calculating NDWI and MNDWI water indices
3. Performing change detection
4. Visualizing lake boundary maps
"""

import numpy as np
import matplotlib.pyplot as plt
from image_reader import create_demo_image, SatelliteImageReader
from water_indices import WaterIndexCalculator, calculate_ndwi, calculate_mndwi
from change_detection import ChangeDetector, detect_change
from visualization import LakeVisualizer
import os


def create_output_directory(output_dir: str = "output"):
    """Create output directory if it doesn't exist."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")
    return output_dir


def demo_basic_water_detection():
    """Demonstrate basic water detection using NDWI and MNDWI."""
    print("\n" + "="*60)
    print("DEMO 1: Basic Water Detection with NDWI and MNDWI")
    print("="*60 + "\n")
    
    # Create synthetic satellite imagery
    print("1. Creating synthetic satellite imagery...")
    reader = create_demo_image(width=512, height=512, lake_radius=120)
    bands = reader.get_all_bands()
    metadata = reader.get_metadata()
    print(f"   Created {metadata['width']}x{metadata['height']} synthetic image")
    print(f"   Lake center: {metadata['lake_center']}, Radius: {metadata['lake_radius']} pixels")
    
    # Calculate water indices
    print("\n2. Calculating water indices...")
    calculator = WaterIndexCalculator()
    
    ndwi = calculator.calculate_ndwi(bands['green'], bands['nir'])
    print("   - NDWI calculated")
    
    mndwi = calculator.calculate_mndwi(bands['green'], bands['swir'])
    print("   - MNDWI calculated")
    
    # Create water masks
    print("\n3. Creating water masks (threshold = 0.0)...")
    ndwi_mask = calculator.threshold_water_mask(ndwi, threshold=0.0)
    mndwi_mask = calculator.threshold_water_mask(mndwi, threshold=0.0)
    print(f"   - NDWI detected {np.sum(ndwi_mask)} water pixels")
    print(f"   - MNDWI detected {np.sum(mndwi_mask)} water pixels")
    
    # Visualize results
    print("\n4. Creating visualizations...")
    output_dir = create_output_directory()
    visualizer = LakeVisualizer(figsize=(15, 10))
    
    # Create comparison plot
    fig = visualizer.create_comparison_plot(
        images=[bands['green'], ndwi, mndwi, ndwi_mask],
        titles=['Green Band', 'NDWI', 'MNDWI', 'Water Mask (NDWI)'],
        cmaps=['Greens', 'RdYlBu', 'RdYlBu', 'Blues'],
        suptitle='Water Detection using NDWI and MNDWI',
        save_path=f'{output_dir}/water_detection.png'
    )
    plt.close(fig)
    
    # Visualize lake boundary
    fig = visualizer.visualize_lake_boundary(
        ndwi_mask,
        title='Detected Lake Boundary',
        background=bands['green'],
        save_path=f'{output_dir}/lake_boundary.png'
    )
    plt.close(fig)
    
    print(f"   Visualizations saved to '{output_dir}/' directory")
    
    return reader, ndwi_mask, mndwi_mask


def demo_change_detection():
    """Demonstrate temporal change detection."""
    print("\n" + "="*60)
    print("DEMO 2: Temporal Change Detection")
    print("="*60 + "\n")
    
    # Create two synthetic images representing different time periods
    print("1. Creating synthetic imagery for two time periods...")
    
    # Time 1: Larger lake (wet season)
    reader_t1 = create_demo_image(width=512, height=512, lake_radius=120)
    bands_t1 = reader_t1.get_all_bands()
    print("   - Time 1: Wet season (larger lake)")
    
    # Time 2: Smaller lake (dry season)
    reader_t2 = create_demo_image(width=512, height=512, lake_radius=90)
    bands_t2 = reader_t2.get_all_bands()
    print("   - Time 2: Dry season (smaller lake)")
    
    # Calculate water masks for both time periods
    print("\n2. Calculating water masks...")
    calculator = WaterIndexCalculator()
    
    ndwi_t1 = calculator.calculate_ndwi(bands_t1['green'], bands_t1['nir'])
    mask_t1 = calculator.threshold_water_mask(ndwi_t1, threshold=0.0)
    print(f"   - Time 1: {np.sum(mask_t1)} water pixels")
    
    ndwi_t2 = calculator.calculate_ndwi(bands_t2['green'], bands_t2['nir'])
    mask_t2 = calculator.threshold_water_mask(ndwi_t2, threshold=0.0)
    print(f"   - Time 2: {np.sum(mask_t2)} water pixels")
    
    # Perform change detection
    print("\n3. Detecting changes...")
    detector = ChangeDetector()
    change_map, stats = detector.detect_water_change(mask_t1, mask_t2)
    
    print("\n   Change Statistics:")
    print(f"   - Stable water: {stats['stable_water_pixels']:,} pixels ({stats['stable_water_percent']:.2f}%)")
    print(f"   - Water loss: {stats['water_loss_pixels']:,} pixels ({stats['water_loss_percent']:.2f}%)")
    print(f"   - Water gain: {stats['water_gain_pixels']:,} pixels ({stats['water_gain_percent']:.2f}%)")
    print(f"   - Net change: {stats['net_change_pixels']:,} pixels ({stats['net_change_percent']:.2f}%)")
    
    # Calculate areas
    print("\n4. Calculating water surface areas (assuming 30m pixel size)...")
    area_t1 = detector.calculate_water_area(mask_t1, pixel_size=30.0)
    area_t2 = detector.calculate_water_area(mask_t2, pixel_size=30.0)
    
    print(f"   - Time 1 area: {area_t1['water_area_km2']:.2f} km²")
    print(f"   - Time 2 area: {area_t2['water_area_km2']:.2f} km²")
    print(f"   - Area change: {area_t2['water_area_km2'] - area_t1['water_area_km2']:.2f} km²")
    
    # Visualize change detection
    print("\n5. Creating visualizations...")
    output_dir = create_output_directory()
    visualizer = LakeVisualizer(figsize=(15, 10))
    
    # Comparison of two time periods
    fig = visualizer.create_comparison_plot(
        images=[mask_t1, mask_t2, change_map],
        titles=['Time 1 (Wet Season)', 'Time 2 (Dry Season)', 'Change Detection'],
        cmaps=['Blues', 'Blues', None],
        suptitle='Temporal Change Detection: Lake Surface Dynamics',
        save_path=f'{output_dir}/change_detection.png'
    )
    plt.close(fig)
    
    # Detailed change map
    fig = visualizer.visualize_change_detection(
        change_map,
        title='Water Surface Change Detection (Time 1 → Time 2)',
        save_path=f'{output_dir}/change_map_detailed.png'
    )
    plt.close(fig)
    
    print(f"   Visualizations saved to '{output_dir}/' directory")
    
    return mask_t1, mask_t2, change_map, stats


def demo_multi_temporal_analysis():
    """Demonstrate multi-temporal analysis across multiple dates."""
    print("\n" + "="*60)
    print("DEMO 3: Multi-Temporal Analysis")
    print("="*60 + "\n")
    
    print("1. Creating synthetic imagery for 5 time periods...")
    
    # Simulate seasonal variations in lake extent
    lake_radii = [110, 130, 115, 95, 105]  # Varying lake sizes
    dates = ['Jan 2023', 'Apr 2023', 'Jul 2023', 'Oct 2023', 'Jan 2024']
    
    masks = []
    calculator = WaterIndexCalculator()
    
    for i, (radius, date) in enumerate(zip(lake_radii, dates)):
        reader = create_demo_image(width=512, height=512, lake_radius=radius)
        bands = reader.get_all_bands()
        ndwi = calculator.calculate_ndwi(bands['green'], bands['nir'])
        mask = calculator.threshold_water_mask(ndwi, threshold=0.0)
        masks.append(mask)
        print(f"   - {date}: Lake radius = {radius} pixels")
    
    # Perform multi-temporal analysis
    print("\n2. Analyzing temporal changes...")
    detector = ChangeDetector()
    results = detector.compare_multiple_dates(masks, dates=dates, pixel_size=30.0)
    
    print("\n   Water Area Over Time:")
    for date, area_info in zip(results['dates'], results['areas']):
        print(f"   - {date}: {area_info['water_area_km2']:.2f} km²")
    
    print(f"\n   Maximum extent: {results['max_area_km2']:.2f} km²")
    print(f"   Minimum extent: {results['min_area_km2']:.2f} km²")
    print(f"   Range: {results['max_area_km2'] - results['min_area_km2']:.2f} km²")
    
    # Visualize time series
    print("\n3. Creating visualizations...")
    output_dir = create_output_directory()
    visualizer = LakeVisualizer()
    
    # Time series plot
    areas_km2 = [area['water_area_km2'] for area in results['areas']]
    fig = visualizer.plot_area_time_series(
        dates=dates,
        areas=areas_km2,
        title='Lake Surface Area Dynamics (2023-2024)',
        save_path=f'{output_dir}/time_series.png'
    )
    plt.close(fig)
    
    # Maximum and minimum extent comparison
    fig = visualizer.create_comparison_plot(
        images=[results['max_extent'], results['min_extent']],
        titles=['Maximum Extent', 'Minimum Extent'],
        cmaps=['Blues', 'Blues'],
        suptitle='Lake Extent Envelope',
        save_path=f'{output_dir}/extent_envelope.png'
    )
    plt.close(fig)
    
    print(f"   Visualizations saved to '{output_dir}/' directory")
    
    return results


def main():
    """Main function to run all demonstrations."""
    print("\n" + "="*60)
    print("Remote Sensing and GIS-Based Lake Monitoring System")
    print("Surface Water Dynamics Assessment")
    print("="*60)
    
    try:
        # Run demonstrations
        demo_basic_water_detection()
        demo_change_detection()
        demo_multi_temporal_analysis()
        
        print("\n" + "="*60)
        print("All demonstrations completed successfully!")
        print("Check the 'output/' directory for generated visualizations.")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\nError during execution: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
