# scripts/cropper.py
"""
Minimal cropper - just crop and save.
"""
import numpy as np
import xarray as xr
from pathlib import Path
import json

from scripts.config import *

def crop_and_save_all(grib_files, centers, output_dir):
    """Crop patches and save as NPY with time metadata."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Open the FIRST file just to get the Lat/Lon grid
    temp_ds = xr.open_dataset(grib_files[0], engine='cfgrib', decode_timedelta=False,)
    lats = temp_ds.latitude.values
    lons = temp_ds.longitude.values
    temp_ds.close()

    # Map indices to actual Lat/Lon coordinates
    center_coords = []
    for r, c in centers:
        lat_val = int(lats[int(r)])
        lon_val = int(lons[int(c)])
        center_coords.append({"lat": lat_val, "lon": lon_val})

    print(f"Processing {len(grib_files)} files into {len(centers)} patches")
     
    metadata = {
        "patch_size": PATCH_SIZE,
        "centers": [[int(r), int(c)] for (r, c) in centers],
        "centers_gps": center_coords,
        "num_files": len(grib_files),
        "timestamps": {}
    }
    
    # Create folders
    folders = []
    for i in range(len(centers)):
        folder = output_path / f"case_{i+1:02d}"
        folder.mkdir(exist_ok=True)
        folders.append(folder)
    
    # Process files
    for frame_num, grib_file in enumerate(grib_files):
        print(f"[{frame_num+1:03d}/{len(grib_files)}] {grib_file.name}")
        
        try:
            ds = xr.open_dataset(grib_file, 
                                 engine='cfgrib', 
                                 decode_timedelta=False,
                                 decode_coords=True,
                                 backend_kwargs={'indexpath': ''})
            
            # Extract timestamp and convert to ISO string
            # MRMS usually uses 'valid_time' or 'time'
            timestamp = ds.valid_time.values if 'valid_time' in ds.coords else ds.time.values
            time_str = np.datetime_as_string(timestamp, unit='m') # format: YYYY-MM-DDTHH:MM
            metadata["timestamps"][frame_num] = time_str
            
            data = ds[list(ds.data_vars)[0]].values
            ds.close()
            
            # Crop and save
            for i, (row, col) in enumerate(centers):
                half = PATCH_SIZE // 2
                patch = data[row-half:row+half, col-half:col+half]
                
                if patch.shape == (PATCH_SIZE, PATCH_SIZE):
                    np.save(folders[i] / f"frame_{frame_num:02d}.npy", patch)
                    
        except Exception as e:
            print(f"  Error: {e}")
    
    #Save metadata at the END so it contains all timestamps
    with open(output_path / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)

def verify_output(output_dir):
    """Quick verification."""
    output_path = Path(output_dir)
    
    if not output_path.exists():
        print(f"Not found: {output_path}")
        return
    
    #Count files
    total = 0
    for folder in output_path.glob("case_*"):
        files = list(folder.glob("*.npy"))
        print(f"{folder.name}: {len(files)} files")
        total += len(files)
    
    print(f"Total: {total} NPY files")