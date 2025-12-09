"""
Module for visualizing lake boundaries and water body analysis results.

This module provides functions to create various visualizations for 
satellite imagery analysis, water indices, and change detection results.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.patches import Patch
from typing import Optional, Tuple, List, Dict
import warnings


class LakeVisualizer:
    """
    A class for creating visualizations of lake monitoring results.
    
    This class provides methods to visualize satellite imagery, water indices,
    water masks, lake boundaries, and temporal changes.
    """
    
    def __init__(self, figsize: Tuple[int, int] = (12, 8)):
        """
        Initialize the LakeVisualizer.
        
        Parameters
        ----------
        figsize : tuple of int
            Default figure size for plots (default: (12, 8))
        """
        self.figsize = figsize
        plt.style.use('default')
    
    def visualize_water_index(self, 
                              water_index: np.ndarray,
                              title: str = "Water Index",
                              cmap: str = "RdYlBu",
                              save_path: Optional[str] = None) -> plt.Figure:
        """
        Visualize a water index (NDWI or MNDWI).
        
        Parameters
        ----------
        water_index : np.ndarray
            Water index array
        title : str
            Plot title (default: "Water Index")
        cmap : str
            Colormap name (default: "RdYlBu")
        save_path : str, optional
            Path to save the figure
        
        Returns
        -------
        plt.Figure
            The created figure
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Plot the water index
        im = ax.imshow(water_index, cmap=cmap, vmin=-1, vmax=1)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.axis('off')
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        cbar.set_label('Water Index Value', rotation=270, labelpad=20)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Figure saved to {save_path}")
        
        return fig
    
    def visualize_water_mask(self,
                            water_mask: np.ndarray,
                            title: str = "Water Mask",
                            background: Optional[np.ndarray] = None,
                            save_path: Optional[str] = None) -> plt.Figure:
        """
        Visualize a binary water mask with optional background.
        
        Parameters
        ----------
        water_mask : np.ndarray
            Binary water mask (0=non-water, 1=water)
        title : str
            Plot title (default: "Water Mask")
        background : np.ndarray, optional
            Background image to overlay the mask on
        save_path : str, optional
            Path to save the figure
        
        Returns
        -------
        plt.Figure
            The created figure
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        
        if background is not None:
            # Display background in grayscale
            ax.imshow(background, cmap='gray', alpha=0.7)
        
        # Create custom colormap for water mask
        cmap = colors.ListedColormap(['none', 'blue'])
        
        # Overlay water mask
        masked_data = np.ma.masked_where(water_mask == 0, water_mask)
        ax.imshow(masked_data, cmap=cmap, alpha=0.6, interpolation='nearest')
        
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.axis('off')
        
        # Add legend
        legend_elements = [Patch(facecolor='blue', alpha=0.6, label='Water')]
        ax.legend(handles=legend_elements, loc='upper right')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Figure saved to {save_path}")
        
        return fig
    
    def visualize_lake_boundary(self,
                               water_mask: np.ndarray,
                               title: str = "Lake Boundary",
                               background: Optional[np.ndarray] = None,
                               boundary_color: str = 'red',
                               save_path: Optional[str] = None) -> plt.Figure:
        """
        Visualize lake boundary with optional background.
        
        Parameters
        ----------
        water_mask : np.ndarray
            Binary water mask
        title : str
            Plot title (default: "Lake Boundary")
        background : np.ndarray, optional
            Background image
        boundary_color : str
            Color for boundary line (default: 'red')
        save_path : str, optional
            Path to save the figure
        
        Returns
        -------
        plt.Figure
            The created figure
        """
        from scipy import ndimage
        
        fig, ax = plt.subplots(figsize=self.figsize)
        
        if background is not None:
            ax.imshow(background, cmap='gray', alpha=0.7)
        else:
            # Create a simple background
            ax.imshow(np.ones_like(water_mask), cmap='gray', vmin=0, vmax=1, alpha=0.3)
        
        # Find boundaries using morphological operations
        boundary = water_mask.astype(np.uint8)
        eroded = ndimage.binary_erosion(boundary)
        boundary_pixels = boundary.astype(bool) & ~eroded
        
        # Define color mapping
        color_map = {
            'red': [1, 0, 0, 1],
            'blue': [0, 0, 1, 1],
            'green': [0, 1, 0, 1]
        }
        
        # Create boundary visualization
        boundary_display = np.zeros((*water_mask.shape, 4))
        boundary_display[boundary_pixels] = color_map.get(boundary_color, [1, 0, 0, 1])  # default to red
        
        # Overlay boundary
        ax.imshow(boundary_display)
        
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.axis('off')
        
        # Add legend
        legend_elements = [Patch(facecolor=boundary_color, label='Lake Boundary')]
        ax.legend(handles=legend_elements, loc='upper right')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Figure saved to {save_path}")
        
        return fig
    
    def visualize_change_detection(self,
                                   change_map: np.ndarray,
                                   title: str = "Water Change Detection",
                                   save_path: Optional[str] = None) -> plt.Figure:
        """
        Visualize change detection results.
        
        Parameters
        ----------
        change_map : np.ndarray
            Change map with values:
            0 = Stable non-water
            1 = Stable water
            2 = Water loss
            3 = Water gain
        title : str
            Plot title (default: "Water Change Detection")
        save_path : str, optional
            Path to save the figure
        
        Returns
        -------
        plt.Figure
            The created figure
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Define custom colormap for change classes
        change_colors = ['#f0f0f0', '#0077be', '#ff6b6b', '#4ecdc4']
        cmap = colors.ListedColormap(change_colors)
        bounds = [0, 1, 2, 3, 4]
        norm = colors.BoundaryNorm(bounds, cmap.N)
        
        # Plot change map
        im = ax.imshow(change_map, cmap=cmap, norm=norm, interpolation='nearest')
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.axis('off')
        
        # Create legend
        legend_elements = [
            Patch(facecolor=change_colors[0], label='Stable Non-Water'),
            Patch(facecolor=change_colors[1], label='Stable Water'),
            Patch(facecolor=change_colors[2], label='Water Loss'),
            Patch(facecolor=change_colors[3], label='Water Gain')
        ]
        ax.legend(handles=legend_elements, loc='upper right', fontsize=10)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Figure saved to {save_path}")
        
        return fig
    
    def create_comparison_plot(self,
                              images: List[np.ndarray],
                              titles: List[str],
                              cmaps: Optional[List[str]] = None,
                              suptitle: str = "Comparison",
                              save_path: Optional[str] = None) -> plt.Figure:
        """
        Create a side-by-side comparison plot of multiple images.
        
        Parameters
        ----------
        images : list of np.ndarray
            List of images to compare
        titles : list of str
            Title for each subplot
        cmaps : list of str, optional
            Colormaps for each image (default: 'viridis' for all)
        suptitle : str
            Overall figure title (default: "Comparison")
        save_path : str, optional
            Path to save the figure
        
        Returns
        -------
        plt.Figure
            The created figure
        """
        n_images = len(images)
        
        if cmaps is None:
            cmaps = ['viridis'] * n_images
        
        if len(titles) != n_images:
            raise ValueError("Number of titles must match number of images")
        
        # Create subplot grid
        cols = min(3, n_images)
        rows = (n_images + cols - 1) // cols
        
        fig, axes = plt.subplots(rows, cols, figsize=(5*cols, 5*rows))
        
        # Ensure axes is always a flat array for consistent indexing
        if n_images == 1:
            axes = np.array([axes])
        else:
            axes = axes.flatten()
        
        for i, (img, title, cmap) in enumerate(zip(images, titles, cmaps)):
            axes[i].imshow(img, cmap=cmap)
            axes[i].set_title(title, fontsize=12, fontweight='bold')
            axes[i].axis('off')
        
        # Hide unused subplots
        for i in range(n_images, len(axes)):
            axes[i].axis('off')
        
        fig.suptitle(suptitle, fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Figure saved to {save_path}")
        
        return fig
    
    def plot_area_time_series(self,
                             dates: List[str],
                             areas: List[float],
                             title: str = "Lake Area Over Time",
                             xlabel: str = "Date",
                             ylabel: str = "Area (km²)",
                             save_path: Optional[str] = None) -> plt.Figure:
        """
        Create a time series plot of lake area.
        
        Parameters
        ----------
        dates : list of str
            Date labels
        areas : list of float
            Area values (in km²)
        title : str
            Plot title (default: "Lake Area Over Time")
        xlabel : str
            X-axis label (default: "Date")
        ylabel : str
            Y-axis label (default: "Area (km²)")
        save_path : str, optional
            Path to save the figure
        
        Returns
        -------
        plt.Figure
            The created figure
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        
        ax.plot(dates, areas, marker='o', linewidth=2, markersize=8, color='#0077be')
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel(xlabel, fontsize=12)
        ax.set_ylabel(ylabel, fontsize=12)
        ax.grid(True, alpha=0.3)
        
        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45, ha='right')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Figure saved to {save_path}")
        
        return fig


# Module-level instance for convenience functions
_default_visualizer = LakeVisualizer()


def plot_water_index(water_index: np.ndarray,
                    title: str = "Water Index",
                    save_path: Optional[str] = None) -> plt.Figure:
    """
    Convenience function to plot a water index.
    
    Parameters
    ----------
    water_index : np.ndarray
        Water index array
    title : str
        Plot title
    save_path : str, optional
        Path to save figure
    
    Returns
    -------
    plt.Figure
        The created figure
    """
    return _default_visualizer.visualize_water_index(water_index, title, save_path=save_path)


def plot_water_mask(water_mask: np.ndarray,
                   title: str = "Water Mask",
                   save_path: Optional[str] = None) -> plt.Figure:
    """
    Convenience function to plot a water mask.
    
    Parameters
    ----------
    water_mask : np.ndarray
        Binary water mask
    title : str
        Plot title
    save_path : str, optional
        Path to save figure
    
    Returns
    -------
    plt.Figure
        The created figure
    """
    return _default_visualizer.visualize_water_mask(water_mask, title, save_path=save_path)


def plot_change_map(change_map: np.ndarray,
                   title: str = "Change Detection",
                   save_path: Optional[str] = None) -> plt.Figure:
    """
    Convenience function to plot change detection results.
    
    Parameters
    ----------
    change_map : np.ndarray
        Change detection map
    title : str
        Plot title
    save_path : str, optional
        Path to save figure
    
    Returns
    -------
    plt.Figure
        The created figure
    """
    return _default_visualizer.visualize_change_detection(change_map, title, save_path=save_path)
