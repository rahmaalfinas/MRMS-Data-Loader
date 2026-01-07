# scripts/analyzer.py
"""
Analyze MRMS data to find storm centers.
"""
import numpy as np
import xarray as xr
from pathlib import Path
from typing import List, Tuple
from scipy import ndimage
from scipy.spatial import KDTree

from scripts.config import *

def load_grib_file(file_path: Path) -> np.ndarray:
    """Load a single GRIB2 file and return numpy array."""
    ds = xr.open_dataset(file_path, engine='cfgrib', decode_timedelta=True)
    var_name = list(ds.data_vars)[0]
    data = ds[var_name].values
    ds.close()
    return data

def find_storm_centers(data: np.ndarray) -> List[Tuple[int, int]]:
    """
    Find centers of storm cells in radar data.
    
    Args:
        data: 2D numpy array of reflectivity
        
    Returns:
        List of (row, col) center coordinates
    """
    # Create binary mask of storms
    storm_mask = data >= THRESHOLD_DBZ
    
    # Label connected components
    labeled, num_storms = ndimage.label(storm_mask)
    
    centers = []
    
    # Calculate center of mass for each storm
    for storm_id in range(1, num_storms + 1):
        rows, cols = np.where(labeled == storm_id)
        
        # Filter small storms
        if len(rows) >= MIN_STORM_PIXELS:
            center_row = int(np.mean(rows))
            center_col = int(np.mean(cols))
            centers.append((center_row, center_col))
    
    return centers

def select_best_centers(all_centers: List[Tuple[int, int]], 
                       data_shape: Tuple[int, int]) -> List[Tuple[int, int]]:
    """
    Select the best N centers that are well-separated.
    
    Args:
        all_centers: All detected storm centers
        data_shape: Shape of original data (rows, cols)
        
    Returns:
        Selected centers (up to MAX_PATCHES)
    """
    if not all_centers:
        return []
    
    # Convert to numpy array
    centers_array = np.array(all_centers)
    
    # Use KDTree for efficient distance checking
    tree = KDTree(centers_array)
    
    selected = []
    half_patch = PATCH_SIZE // 2
    
    for center in centers_array:
        row, col = center
        
        # Check if within bounds
        if (row - half_patch < 0 or row + half_patch >= data_shape[0] or
            col - half_patch < 0 or col + half_patch >= data_shape[1]):
            continue
        
        # Check distance to already selected centers
        too_close = False
        for sel_row, sel_col in selected:
            distance = np.sqrt((row - sel_row)**2 + (col - sel_col)**2)
            if distance < MIN_DISTANCE:
                too_close = True
                break
        
        if not too_close:
            selected.append((row, col))
            
            # Stop if we have enough
            if len(selected) >= MAX_PATCHES:
                break
    
    return selected

def analyze_sample_files(sample_files: List[Path]) -> List[Tuple[int, int]]:
    """
    Analyze multiple files to find persistent storm locations.
    
    Args:
        sample_files: List of GRIB2 files to analyze
        
    Returns:
        Best storm centers across the sample
    """
    all_detected_centers = []
    
    for i, file_path in enumerate(sample_files[:SAMPLE_FILES], 1):
        print(f"Analyzing sample {i}/{len(sample_files[:SAMPLE_FILES])}: {file_path.name}")
        
        try:
            data = load_grib_file(file_path)
            centers = find_storm_centers(data)
            all_detected_centers.extend(centers)
            
            print(f"  Found {len(centers)} storms")
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    # Select best centers from all detected
    if all_detected_centers:
        # Load first file to get data shape
        data = load_grib_file(sample_files[0])
        best_centers = select_best_centers(all_detected_centers, data.shape)
        
        print(f"\n📊 Analysis complete:")
        print(f"  Total storms detected: {len(all_detected_centers)}")
        print(f"  Selected best centers: {len(best_centers)}")
        
        return best_centers
    
    return []