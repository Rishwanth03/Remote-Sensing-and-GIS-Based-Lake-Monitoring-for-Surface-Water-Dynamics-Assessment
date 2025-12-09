"""
Module for reading and processing satellite imagery.

This module provides functionality to read satellite imagery from various
sources and prepare it for water index calculations and change detection.
"""

import numpy as np
from typing import Tuple, Optional, Union
import warnings


class SatelliteImageReader:
    """
    A class for reading and processing satellite imagery for water body analysis.
    
    This class handles the loading of satellite imagery bands (particularly
    green, NIR, and SWIR bands needed for water index calculations).
    """
    
    def __init__(self):
        """Initialize the SatelliteImageReader."""
        self.bands = {}
        self.metadata = {}
    
    def read_bands_from_array(self, 
                              green: np.ndarray, 
                              nir: np.ndarray, 
                              swir: Optional[np.ndarray] = None,
                              metadata: Optional[dict] = None) -> None:
        """
        Read satellite bands from numpy arrays.
        
        Parameters
        ----------
        green : np.ndarray
            Green band (typically Band 3 in Landsat, Band 3 in Sentinel-2)
        nir : np.ndarray
            Near Infrared band (Band 5 in Landsat 8, Band 8 in Sentinel-2)
        swir : np.ndarray, optional
            Short Wave Infrared band (Band 6 in Landsat 8, Band 11 in Sentinel-2)
            Required for MNDWI calculation
        metadata : dict, optional
            Additional metadata about the imagery
        """
        if green.shape != nir.shape:
            raise ValueError("Green and NIR bands must have the same dimensions")
        
        if swir is not None and swir.shape != green.shape:
            raise ValueError("SWIR band must have the same dimensions as other bands")
        
        self.bands['green'] = green.astype(np.float32)
        self.bands['nir'] = nir.astype(np.float32)
        
        if swir is not None:
            self.bands['swir'] = swir.astype(np.float32)
        
        if metadata:
            self.metadata = metadata
    
    def create_synthetic_image(self, 
                               width: int = 512, 
                               height: int = 512,
                               lake_center: Tuple[int, int] = None,
                               lake_radius: int = 100) -> None:
        """
        Create synthetic satellite imagery for testing and demonstration.
        
        This creates artificial bands simulating a lake scene with vegetation
        and water bodies.
        
        Parameters
        ----------
        width : int
            Width of the synthetic image (default: 512)
        height : int
            Height of the synthetic image (default: 512)
        lake_center : tuple of int, optional
            (y, x) coordinates of the lake center. If None, uses image center
        lake_radius : int
            Radius of the synthetic lake (default: 100)
        """
        if lake_center is None:
            lake_center = (height // 2, width // 2)
        
        # Create coordinate grids
        y, x = np.ogrid[:height, :width]
        
        # Calculate distance from lake center
        distance_from_center = np.sqrt((x - lake_center[1])**2 + (y - lake_center[0])**2)
        
        # Create water mask (circular lake)
        water_mask = distance_from_center <= lake_radius
        
        # Initialize bands with land/vegetation values
        green_band = np.random.uniform(0.1, 0.3, (height, width))
        nir_band = np.random.uniform(0.4, 0.6, (height, width))
        swir_band = np.random.uniform(0.3, 0.5, (height, width))
        
        # Set water pixel values (water has low reflectance, especially in NIR/SWIR)
        green_band[water_mask] = np.random.uniform(0.05, 0.15, water_mask.sum())
        nir_band[water_mask] = np.random.uniform(0.01, 0.05, water_mask.sum())
        swir_band[water_mask] = np.random.uniform(0.01, 0.03, water_mask.sum())
        
        # Add some noise for realism
        green_band += np.random.normal(0, 0.02, (height, width))
        nir_band += np.random.normal(0, 0.02, (height, width))
        swir_band += np.random.normal(0, 0.02, (height, width))
        
        # Clip values to valid range [0, 1]
        green_band = np.clip(green_band, 0, 1)
        nir_band = np.clip(nir_band, 0, 1)
        swir_band = np.clip(swir_band, 0, 1)
        
        self.bands['green'] = green_band.astype(np.float32)
        self.bands['nir'] = nir_band.astype(np.float32)
        self.bands['swir'] = swir_band.astype(np.float32)
        
        self.metadata = {
            'width': width,
            'height': height,
            'lake_center': lake_center,
            'lake_radius': lake_radius,
            'synthetic': True
        }
    
    def get_band(self, band_name: str) -> np.ndarray:
        """
        Retrieve a specific band.
        
        Parameters
        ----------
        band_name : str
            Name of the band ('green', 'nir', or 'swir')
        
        Returns
        -------
        np.ndarray
            The requested band array
        
        Raises
        ------
        ValueError
            If the requested band is not available
        """
        if band_name not in self.bands:
            raise ValueError(f"Band '{band_name}' not found. Available bands: {list(self.bands.keys())}")
        
        return self.bands[band_name]
    
    def get_all_bands(self) -> dict:
        """
        Get all loaded bands.
        
        Returns
        -------
        dict
            Dictionary containing all loaded bands
        """
        return self.bands.copy()
    
    def get_metadata(self) -> dict:
        """
        Get image metadata.
        
        Returns
        -------
        dict
            Dictionary containing image metadata
        """
        return self.metadata.copy()


def load_satellite_image(green: np.ndarray, 
                         nir: np.ndarray, 
                         swir: Optional[np.ndarray] = None) -> SatelliteImageReader:
    """
    Convenience function to load satellite imagery from numpy arrays.
    
    Parameters
    ----------
    green : np.ndarray
        Green band array
    nir : np.ndarray
        Near Infrared band array
    swir : np.ndarray, optional
        Short Wave Infrared band array
    
    Returns
    -------
    SatelliteImageReader
        Initialized reader with loaded bands
    """
    reader = SatelliteImageReader()
    reader.read_bands_from_array(green, nir, swir)
    return reader


def create_demo_image(width: int = 512, 
                      height: int = 512,
                      lake_radius: int = 100) -> SatelliteImageReader:
    """
    Create a synthetic satellite image for demonstration purposes.
    
    Parameters
    ----------
    width : int
        Image width (default: 512)
    height : int
        Image height (default: 512)
    lake_radius : int
        Radius of the synthetic lake (default: 100)
    
    Returns
    -------
    SatelliteImageReader
        Reader with synthetic imagery
    """
    reader = SatelliteImageReader()
    reader.create_synthetic_image(width, height, lake_radius=lake_radius)
    return reader
