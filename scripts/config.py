# scripts/config.py
"""
Configuration parameters for MRMS data processing.
Adjust these values based on your specific needs.
"""
from pathlib import Path

# File paths (Update these for your system)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw_mrms"
OUTPUT_DIR = PROJECT_ROOT / "data" / "npy_patches"
COMPRESSED_DIR = PROJECT_ROOT/ "data" / "downloaded_data"

# Patch settings
PATCH_SIZE = 1468  # Size of square patches to extract

# Storm detection settings
THRESHOLD_DBZ = 35      # Minimum reflectivity to consider as storm (dBZ)
MIN_STORM_PIXELS = 100  # Minimum storm size to keep (pixels)
MIN_DISTANCE = 500      # Minimum distance between selected centers (pixels)

# Processing settings
MAX_PATCHES = 6         # Maximum number of patches to extract
SAMPLE_FILES = 1        # Number of files to sample for storm detection