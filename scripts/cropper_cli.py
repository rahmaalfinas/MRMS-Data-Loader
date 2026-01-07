# scripts/cropper_cli.py
"""
Simple cropping interface.
"""
import json
from pathlib import Path

from scripts.config import *
from scripts.cropper import crop_and_save_all, verify_output

def run_cropping():
    """Load centers and crop."""
    # Load analysis
    analysis_file = Path(OUTPUT_DIR) / "analysis_results.json"
    if not analysis_file.exists():
        print("Run 'python main.py analyze' first")
        return
    
    with open(analysis_file, "r") as f:
        data = json.load(f)
    
    centers = [(r, c) for [r, c] in data["centers"]]
    
    # Get files
    files = sorted(Path(RAW_DATA_DIR).glob("*.grib2"))
    
    # Confirm
    print(f"Crop {len(files)} files into {len(centers)} patches?")
    if input("Continue with cropping? [y/N]: ").lower() != 'y':
        return
    
    # Crop
    crop_and_save_all(files, centers, OUTPUT_DIR)
    
    # Verify
    verify_output(OUTPUT_DIR)