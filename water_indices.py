"""
Module for calculating water indices from satellite imagery.

This module implements NDWI (Normalized Difference Water Index) and 
MNDWI (Modified Normalized Difference Water Index) calculations for 
identifying water bodies in satellite imagery.
"""

import numpy as np
from typing import Optional, Tuple
import warnings


class WaterIndexCalculator:
    """
    A class for calculating water indices from satellite imagery.
    
    This class provides methods to calculate NDWI and MNDWI, which are
    widely used for water body detection and mapping from multispectral
    satellite imagery.
    """
    
    def __init__(self):
        """Initialize the WaterIndexCalculator."""
        pass
    
    @staticmethod
    def calculate_ndwi(green: np.ndarray, nir: np.ndarray) -> np.ndarray:
        """
        Calculate Normalized Difference Water Index (NDWI).
        
        NDWI = (Green - NIR) / (Green + NIR)
        
        NDWI is useful for detecting surface water and delineating water bodies.
        Positive values typically indicate water, while negative values indicate
        vegetation or dry land.
        
        Parameters
        ----------
        green : np.ndarray
            Green band reflectance values
        nir : np.ndarray
            Near Infrared band reflectance values
        
        Returns
        -------
        np.ndarray
            NDWI values ranging from -1 to 1
        
        References
        ----------
        McFeeters, S.K., 1996. The use of the Normalized Difference Water Index (NDWI)
        in the delineation of open water features. International Journal of Remote Sensing,
        17(7), pp.1425-1432.
        """
        if green.shape != nir.shape:
            raise ValueError("Green and NIR bands must have the same shape")
        
        # Avoid division by zero
        numerator = green - nir
        denominator = green + nir
        
        # Handle division by zero
        with np.errstate(divide='ignore', invalid='ignore'):
            ndwi = np.divide(numerator, denominator)
            # Set pixels where denominator is zero to NaN
            ndwi[denominator == 0] = np.nan
        
        return ndwi
    
    @staticmethod
    def calculate_mndwi(green: np.ndarray, swir: np.ndarray) -> np.ndarray:
        """
        Calculate Modified Normalized Difference Water Index (MNDWI).
        
        MNDWI = (Green - SWIR) / (Green + SWIR)
        
        MNDWI is more effective than NDWI for suppressing built-up land noise
        and enhancing open water features. It uses SWIR instead of NIR.
        
        Parameters
        ----------
        green : np.ndarray
            Green band reflectance values
        swir : np.ndarray
            Short Wave Infrared band reflectance values
        
        Returns
        -------
        np.ndarray
            MNDWI values ranging from -1 to 1
        
        References
        ----------
        Xu, H., 2006. Modification of normalised difference water index (NDWI) to enhance
        open water features in remotely sensed imagery. International Journal of Remote
        Sensing, 27(14), pp.3025-3033.
        """
        if green.shape != swir.shape:
            raise ValueError("Green and SWIR bands must have the same shape")
        
        # Avoid division by zero
        numerator = green - swir
        denominator = green + swir
        
        # Handle division by zero
        with np.errstate(divide='ignore', invalid='ignore'):
            mndwi = np.divide(numerator, denominator)
            # Set pixels where denominator is zero to NaN
            mndwi[denominator == 0] = np.nan
        
        return mndwi
    
    @staticmethod
    def threshold_water_mask(index: np.ndarray, 
                             threshold: float = 0.0,
                             use_otsu: bool = False) -> np.ndarray:
        """
        Create a binary water mask from a water index using thresholding.
        
        Parameters
        ----------
        index : np.ndarray
            Water index array (NDWI or MNDWI)
        threshold : float, optional
            Threshold value for classification. Pixels with index > threshold
            are classified as water (default: 0.0)
        use_otsu : bool, optional
            If True, automatically determine threshold using Otsu's method
            (default: False)
        
        Returns
        -------
        np.ndarray
            Binary mask where 1 indicates water and 0 indicates non-water
        """
        # Remove NaN values for processing
        valid_mask = ~np.isnan(index)
        valid_index = index[valid_mask]
        
        if use_otsu:
            try:
                from skimage.filters import threshold_otsu
                # Normalize to 0-255 range for Otsu
                normalized = ((valid_index - valid_index.min()) / 
                             (valid_index.max() - valid_index.min()) * 255).astype(np.uint8)
                threshold_value = threshold_otsu(normalized)
                # Convert back to original range
                threshold = (threshold_value / 255.0 * 
                           (valid_index.max() - valid_index.min()) + valid_index.min())
            except ImportError:
                warnings.warn("scikit-image not available. Using default threshold.")
        
        # Create binary mask
        water_mask = np.zeros_like(index, dtype=bool)
        water_mask[valid_mask] = index[valid_mask] > threshold
        
        return water_mask.astype(np.uint8)
    
    def calculate_water_extent(self, 
                               green: np.ndarray, 
                               nir: np.ndarray, 
                               swir: Optional[np.ndarray] = None,
                               method: str = 'ndwi',
                               threshold: float = 0.0) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calculate water extent using specified method.
        
        Parameters
        ----------
        green : np.ndarray
            Green band
        nir : np.ndarray
            Near Infrared band
        swir : np.ndarray, optional
            Short Wave Infrared band (required for MNDWI)
        method : str
            Method to use: 'ndwi' or 'mndwi' (default: 'ndwi')
        threshold : float
            Threshold value for water classification (default: 0.0)
        
        Returns
        -------
        tuple of np.ndarray
            (water_index, water_mask) where water_index is the calculated index
            and water_mask is the binary classification
        """
        if method.lower() == 'ndwi':
            water_index = self.calculate_ndwi(green, nir)
        elif method.lower() == 'mndwi':
            if swir is None:
                raise ValueError("SWIR band is required for MNDWI calculation")
            water_index = self.calculate_mndwi(green, swir)
        else:
            raise ValueError(f"Unknown method: {method}. Use 'ndwi' or 'mndwi'")
        
        water_mask = self.threshold_water_mask(water_index, threshold)
        
        return water_index, water_mask


def calculate_ndwi(green: np.ndarray, nir: np.ndarray) -> np.ndarray:
    """
    Convenience function to calculate NDWI.
    
    Parameters
    ----------
    green : np.ndarray
        Green band reflectance values
    nir : np.ndarray
        Near Infrared band reflectance values
    
    Returns
    -------
    np.ndarray
        NDWI values
    """
    calculator = WaterIndexCalculator()
    return calculator.calculate_ndwi(green, nir)


def calculate_mndwi(green: np.ndarray, swir: np.ndarray) -> np.ndarray:
    """
    Convenience function to calculate MNDWI.
    
    Parameters
    ----------
    green : np.ndarray
        Green band reflectance values
    swir : np.ndarray
        Short Wave Infrared band reflectance values
    
    Returns
    -------
    np.ndarray
        MNDWI values
    """
    calculator = WaterIndexCalculator()
    return calculator.calculate_mndwi(green, swir)


def extract_water_mask(water_index: np.ndarray, 
                       threshold: float = 0.0,
                       use_otsu: bool = False) -> np.ndarray:
    """
    Convenience function to extract water mask from water index.
    
    Parameters
    ----------
    water_index : np.ndarray
        Water index array (NDWI or MNDWI)
    threshold : float, optional
        Threshold value (default: 0.0)
    use_otsu : bool, optional
        Use automatic Otsu thresholding (default: False)
    
    Returns
    -------
    np.ndarray
        Binary water mask
    """
    calculator = WaterIndexCalculator()
    return calculator.threshold_water_mask(water_index, threshold, use_otsu)
