# Remote Sensing and GIS-Based Lake Monitoring for Surface Water Dynamics Assessment

This project integrates satellite data with GIS analysis to map lake boundaries and examine how water surfaces change across seasons or years. It supports effective water resource planning and environmental management.

## Overview

The system provides a complete Python-based workflow for:
- **Reading and processing satellite imagery** from multispectral bands
- **Calculating water indices** (NDWI and MNDWI) to identify water bodies
- **Performing temporal change detection** to track lake surface dynamics
- **Visualizing lake boundaries and changes** with publication-quality maps

## Features

### 1. Satellite Imagery Processing (`image_reader.py`)
- Read multispectral satellite bands (Green, NIR, SWIR)
- Support for various satellite platforms (Landsat, Sentinel-2, etc.)
- Synthetic image generation for testing and demonstrations

### 2. Water Index Calculation (`water_indices.py`)
- **NDWI (Normalized Difference Water Index)**: `(Green - NIR) / (Green + NIR)`
- **MNDWI (Modified NDWI)**: `(Green - SWIR) / (Green + SWIR)`
- Automatic and manual thresholding for water classification
- Support for Otsu's method for optimal threshold selection

### 3. Change Detection (`change_detection.py`)
- Temporal change analysis between multiple dates
- Classification of change types:
  - Stable water
  - Stable non-water
  - Water loss (drying)
  - Water gain (flooding)
- Water surface area calculations
- Multi-temporal trend analysis

### 4. Visualization (`visualization.py`)
- Water index visualization with color scales
- Lake boundary delineation
- Change detection maps
- Time series plots
- Side-by-side comparison plots

## Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Rishwanth03/Remote-Sensing-and-GIS-Based-Lake-Monitoring-for-Surface-Water-Dynamics-Assessment.git
cd Remote-Sensing-and-GIS-Based-Lake-Monitoring-for-Surface-Water-Dynamics-Assessment
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

Run the demonstration script to see all features in action:

```bash
python main.py
```

This will:
1. Generate synthetic satellite imagery
2. Calculate NDWI and MNDWI indices
3. Perform change detection analysis
4. Create visualizations in the `output/` directory

## Usage Examples

### Example 1: Basic Water Detection

```python
from image_reader import create_demo_image
from water_indices import WaterIndexCalculator

# Create synthetic imagery
reader = create_demo_image(width=512, height=512, lake_radius=100)
bands = reader.get_all_bands()

# Calculate NDWI
calculator = WaterIndexCalculator()
ndwi = calculator.calculate_ndwi(bands['green'], bands['nir'])

# Create water mask
water_mask = calculator.threshold_water_mask(ndwi, threshold=0.0)
```

### Example 2: Change Detection

```python
from change_detection import ChangeDetector

# Compare two time periods
detector = ChangeDetector()
change_map, stats = detector.detect_water_change(mask_t1, mask_t2)

# Get statistics
print(f"Water loss: {stats['water_loss_percent']:.2f}%")
print(f"Water gain: {stats['water_gain_percent']:.2f}%")
```

### Example 3: Visualization

```python
from visualization import LakeVisualizer

visualizer = LakeVisualizer()

# Visualize water index
fig = visualizer.visualize_water_index(ndwi, title="NDWI Analysis")

# Visualize lake boundary
fig = visualizer.visualize_lake_boundary(water_mask, title="Lake Boundary")

# Visualize changes
fig = visualizer.visualize_change_detection(change_map, title="Surface Water Changes")
```

### Example 4: Multi-Temporal Analysis

```python
from change_detection import ChangeDetector

detector = ChangeDetector()
results = detector.compare_multiple_dates(
    masks=[mask1, mask2, mask3],
    dates=['Jan 2023', 'Jul 2023', 'Jan 2024'],
    pixel_size=30.0
)

# Access results
for date, area in zip(results['dates'], results['areas']):
    print(f"{date}: {area['water_area_km2']:.2f} km²")
```

## Module Documentation

### image_reader.py

**Key Classes:**
- `SatelliteImageReader`: Main class for reading and managing satellite imagery

**Key Functions:**
- `create_demo_image()`: Generate synthetic satellite imagery for testing
- `load_satellite_image()`: Load real satellite imagery from arrays

### water_indices.py

**Key Classes:**
- `WaterIndexCalculator`: Calculate water indices and create water masks

**Key Functions:**
- `calculate_ndwi()`: Compute Normalized Difference Water Index
- `calculate_mndwi()`: Compute Modified NDWI
- `extract_water_mask()`: Create binary water mask from indices

### change_detection.py

**Key Classes:**
- `ChangeDetector`: Analyze temporal changes in water bodies

**Key Functions:**
- `detect_water_change()`: Compare water masks between two dates
- `calculate_water_area()`: Compute water surface area
- `compare_multiple_dates()`: Multi-temporal analysis

### visualization.py

**Key Classes:**
- `LakeVisualizer`: Create various visualizations

**Key Functions:**
- `visualize_water_index()`: Plot water indices
- `visualize_lake_boundary()`: Display lake boundaries
- `visualize_change_detection()`: Show change detection results
- `plot_area_time_series()`: Create time series plots

## Scientific Background

### Water Indices

**NDWI (Normalized Difference Water Index)**
- Formula: `(Green - NIR) / (Green + NIR)`
- Reference: McFeeters, S.K. (1996)
- Best for: Open water detection

**MNDWI (Modified NDWI)**
- Formula: `(Green - SWIR) / (Green + SWIR)`
- Reference: Xu, H. (2006)
- Best for: Water detection in urban areas, reduces built-up land noise

### Change Detection

The system classifies pixel-level changes into four categories:
1. **Stable water**: Remains water in both periods
2. **Stable non-water**: Remains non-water in both periods
3. **Water loss**: Transitions from water to non-water (drying/recession)
4. **Water gain**: Transitions from non-water to water (flooding/expansion)

## Output Files

Running `main.py` generates the following visualizations in the `output/` directory:
- `water_detection.png`: Water index comparison (Green, NDWI, MNDWI, Water Mask)
- `lake_boundary.png`: Detected lake boundary overlay
- `change_detection.png`: Temporal comparison and change map
- `change_map_detailed.png`: Detailed change classification
- `time_series.png`: Lake area over time
- `extent_envelope.png`: Maximum and minimum lake extent

## Applications

This system can be applied to:
- **Water resource management**: Monitor reservoir and lake levels
- **Drought assessment**: Track water body recession during dry periods
- **Flood mapping**: Identify flooded areas after heavy rainfall
- **Environmental monitoring**: Study seasonal and long-term changes in wetlands
- **Climate change studies**: Assess impacts on surface water resources
- **Agricultural planning**: Monitor irrigation water availability

## Data Requirements

For real-world applications, you'll need:
- Multispectral satellite imagery with at least:
  - Green band (e.g., Landsat 8 Band 3, Sentinel-2 Band 3)
  - NIR band (e.g., Landsat 8 Band 5, Sentinel-2 Band 8)
  - SWIR band for MNDWI (e.g., Landsat 8 Band 6, Sentinel-2 Band 11)
- Co-registered images from different dates for change detection
- Atmospherically corrected surface reflectance data (recommended)

## Satellite Data Sources

- **Landsat 8/9**: Free access via USGS Earth Explorer
- **Sentinel-2**: Free access via Copernicus Open Access Hub
- **MODIS**: Free access via NASA EARTHDATA

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

This project implements well-established remote sensing techniques for water body detection and monitoring, based on research by McFeeters (1996) and Xu (2006).

## Contact

For questions or collaboration opportunities, please open an issue on GitHub.
