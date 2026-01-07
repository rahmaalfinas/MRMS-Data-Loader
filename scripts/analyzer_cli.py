# scripts/analyzer_cli.py
"""
Simple analyzer - find storms and save centers.
"""
import numpy as np
import json
from pathlib import Path

from scripts.config import *
from scripts.analyzer import load_grib_file, find_storm_centers, select_best_centers

def run_analysis():
    """Find storms and save centers."""
    print("🔍 Analyzing data for finding storm centre...")
    
    # Get files
    files = sorted(Path(RAW_DATA_DIR).glob("*.grib2"))
    if not files:
        print(f"No files in {RAW_DATA_DIR}")
        return
    
    # Analyze first file
    data = load_grib_file(files[0])
    centers = find_storm_centers(data)
    best = select_best_centers(centers, data.shape)
    
    print(f"Found {len(best)} good storm centers")
    for i, (r, c) in enumerate(best):
        print(f"  {i+1}: ({r}, {c})")
    
    # Save
    centers_data = [[int(r), int(c)] for (r, c) in best]
    output = Path(OUTPUT_DIR) / "analysis_results.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output, "w") as f:
        json.dump({"centers": centers_data}, f, indent=2)
    
    print(f"✅ Saved to {output}")
    
    # Ask for visualization
    try:
        from utils.visualization import plot_storm_centers
        if input("Show and save plot? [y/N]: ").lower() == 'y':
            plot_storm_centers(data, best, PATCH_SIZE, OUTPUT_DIR)
    except:
        pass