"""
Module for detecting changes in water bodies over time.

This module provides functionality for analyzing temporal changes in lake
surface water extent using multi-temporal satellite imagery.
"""

import numpy as np
from typing import Tuple, Dict, Optional, List
import warnings


class ChangeDetector:
    """
    A class for detecting changes in water bodies between different time periods.
    
    This class analyzes changes in lake extent by comparing water masks or
    water indices from different time periods.
    """
    
    def __init__(self):
        """Initialize the ChangeDetector."""
        pass
    
    @staticmethod
    def detect_water_change(mask_t1: np.ndarray, 
                           mask_t2: np.ndarray) -> Tuple[np.ndarray, Dict[str, float]]:
        """
        Detect changes in water extent between two time periods.
        
        This method classifies pixels into four categories:
        - Stable water: Water in both time periods
        - Stable non-water: Non-water in both time periods  
        - Water gain: Non-water to water
        - Water loss: Water to non-water
        
        Parameters
        ----------
        mask_t1 : np.ndarray
            Binary water mask from time period 1 (0=non-water, 1=water)
        mask_t2 : np.ndarray
            Binary water mask from time period 2 (0=non-water, 1=water)
        
        Returns
        -------
        change_map : np.ndarray
            Change classification map with values:
            0 = Stable non-water
            1 = Stable water
            2 = Water loss (was water, now non-water)
            3 = Water gain (was non-water, now water)
        statistics : dict
            Dictionary containing change statistics
        """
        if mask_t1.shape != mask_t2.shape:
            raise ValueError("Input masks must have the same shape")
        
        # Convert to boolean for easier logic
        water_t1 = mask_t1.astype(bool)
        water_t2 = mask_t2.astype(bool)
        
        # Create change map
        change_map = np.zeros_like(mask_t1, dtype=np.uint8)
        
        # Classify changes
        stable_water = water_t1 & water_t2
        stable_non_water = ~water_t1 & ~water_t2
        water_loss = water_t1 & ~water_t2
        water_gain = ~water_t1 & water_t2
        
        change_map[stable_non_water] = 0
        change_map[stable_water] = 1
        change_map[water_loss] = 2
        change_map[water_gain] = 3
        
        # Calculate statistics
        total_pixels = mask_t1.size
        stats = {
            'stable_water_pixels': int(stable_water.sum()),
            'stable_non_water_pixels': int(stable_non_water.sum()),
            'water_loss_pixels': int(water_loss.sum()),
            'water_gain_pixels': int(water_gain.sum()),
            'stable_water_percent': float(stable_water.sum() / total_pixels * 100),
            'water_loss_percent': float(water_loss.sum() / total_pixels * 100),
            'water_gain_percent': float(water_gain.sum() / total_pixels * 100),
            'net_change_pixels': int(water_gain.sum() - water_loss.sum()),
            'net_change_percent': float((water_gain.sum() - water_loss.sum()) / total_pixels * 100)
        }
        
        return change_map, stats
    
    @staticmethod
    def calculate_water_area(water_mask: np.ndarray, 
                            pixel_size: float = 30.0) -> Dict[str, float]:
        """
        Calculate water surface area from a binary water mask.
        
        Parameters
        ----------
        water_mask : np.ndarray
            Binary water mask (0=non-water, 1=water)
        pixel_size : float
            Pixel size in meters (default: 30.0 for Landsat)
        
        Returns
        -------
        dict
            Dictionary containing area statistics:
            - water_pixels: Number of water pixels
            - water_area_m2: Water area in square meters
            - water_area_km2: Water area in square kilometers
        """
        water_pixels = int(np.sum(water_mask))
        pixel_area_m2 = pixel_size ** 2
        water_area_m2 = water_pixels * pixel_area_m2
        water_area_km2 = water_area_m2 / 1e6
        
        return {
            'water_pixels': water_pixels,
            'water_area_m2': water_area_m2,
            'water_area_km2': water_area_km2
        }
    
    def compare_multiple_dates(self, 
                               masks: List[np.ndarray],
                               dates: Optional[List[str]] = None,
                               pixel_size: float = 30.0) -> Dict:
        """
        Compare water extent across multiple dates.
        
        Parameters
        ----------
        masks : list of np.ndarray
            List of binary water masks from different dates
        dates : list of str, optional
            List of date strings corresponding to each mask
        pixel_size : float
            Pixel size in meters (default: 30.0)
        
        Returns
        -------
        dict
            Dictionary containing:
            - areas: List of water area for each date
            - changes: Pairwise changes between consecutive dates
            - max_extent: Maximum water extent across all dates
            - min_extent: Minimum water extent across all dates
        """
        if len(masks) < 2:
            raise ValueError("At least 2 masks are required for comparison")
        
        # Check all masks have same shape
        shapes = [mask.shape for mask in masks]
        if len(set(shapes)) > 1:
            raise ValueError("All masks must have the same shape")
        
        if dates is None:
            dates = [f"Date_{i+1}" for i in range(len(masks))]
        
        # Calculate area for each date
        areas = []
        for mask in masks:
            area_stats = self.calculate_water_area(mask, pixel_size)
            areas.append(area_stats)
        
        # Calculate pairwise changes
        changes = []
        for i in range(len(masks) - 1):
            change_map, stats = self.detect_water_change(masks[i], masks[i+1])
            changes.append({
                'from_date': dates[i],
                'to_date': dates[i+1],
                'change_map': change_map,
                'statistics': stats
            })
        
        # Find maximum and minimum extent
        max_extent = np.zeros_like(masks[0], dtype=np.uint8)
        min_extent = np.ones_like(masks[0], dtype=np.uint8)
        
        for mask in masks:
            max_extent = np.maximum(max_extent, mask)
            min_extent = np.minimum(min_extent, mask)
        
        return {
            'dates': dates,
            'areas': areas,
            'changes': changes,
            'max_extent': max_extent,
            'min_extent': min_extent,
            'max_area_km2': self.calculate_water_area(max_extent, pixel_size)['water_area_km2'],
            'min_area_km2': self.calculate_water_area(min_extent, pixel_size)['water_area_km2']
        }
    
    @staticmethod
    def calculate_change_intensity(index_t1: np.ndarray,
                                   index_t2: np.ndarray) -> np.ndarray:
        """
        Calculate the intensity of change in water index values.
        
        Parameters
        ----------
        index_t1 : np.ndarray
            Water index from time period 1
        index_t2 : np.ndarray
            Water index from time period 2
        
        Returns
        -------
        np.ndarray
            Difference in water index (index_t2 - index_t1)
            Positive values indicate increase in water likelihood
            Negative values indicate decrease in water likelihood
        """
        if index_t1.shape != index_t2.shape:
            raise ValueError("Input indices must have the same shape")
        
        return index_t2 - index_t1


def detect_change(mask_t1: np.ndarray, mask_t2: np.ndarray) -> Tuple[np.ndarray, Dict]:
    """
    Convenience function to detect changes between two water masks.
    
    Parameters
    ----------
    mask_t1 : np.ndarray
        Water mask from time 1
    mask_t2 : np.ndarray
        Water mask from time 2
    
    Returns
    -------
    tuple
        (change_map, statistics)
    """
    detector = ChangeDetector()
    return detector.detect_water_change(mask_t1, mask_t2)


def calculate_area(water_mask: np.ndarray, pixel_size: float = 30.0) -> Dict[str, float]:
    """
    Convenience function to calculate water area.
    
    Parameters
    ----------
    water_mask : np.ndarray
        Binary water mask
    pixel_size : float
        Pixel size in meters (default: 30.0)
    
    Returns
    -------
    dict
        Area statistics
    """
    detector = ChangeDetector()
    return detector.calculate_water_area(water_mask, pixel_size)
