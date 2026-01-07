# MRMS Data Processor

Process MRMS radar data and extract storm patches.
MRMS DATA 
https://www.nssl.noaa.gov/projects/mrms/

MRMS Download:
https://mrms.ncep.noaa.gov/2D/

This code provides extraction from grib2.gz format to grib2 format then analyzing potential storm centers and cropping it into patches with the size needed for nowcasting models (Pysteps, DeepRaNE, Nowcastnet) input.

## Structure:

## Usage:

1. **Update paths** in `scripts/config.py`

2. **Run the pipeline**:
```bash
python main.py process
```

3. **Or run modules independently:**

```bash
python main.py [command]
```
analyze : Analyze data and show storm patch locations

process : Run full pipeline (analyze + crop)

extract : Extract .grib2.gz files only

crop : Crop patches only (requires analysis first)

help : Show help

4. **Configuration:**

Edit scripts/config.py to adjust:

- THRESHOLD_DBZ: Storm detection threshold

- MIN_DISTANCE: Minimum distance between storm center to be selected

- MAX_PATCHES: Maximum number of patches to extract

- PATCH_SIZE: Size of square patches to extract

- DIRECTORY: 
    1. PROJECT_ROOT
    2. RAW_DATA_DIR
    3. OUTPUT_DIR
    4. COMPRESSED_DIR
    
