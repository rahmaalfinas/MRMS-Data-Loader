# scripts/extractor.py
"""
Extract .grib2.gz files to .grib2 format.
"""
import gzip
import shutil
from pathlib import Path
from typing import List
import sys

def extract_grib_files(gz_dir: str, output_dir: str) -> List[Path]:
    """
    Extract all .grib2.gz files to output directory.
    
    Args:
        gz_dir: Directory containing .grib2.gz files
        output_dir: Directory to save extracted .grib2 files
        
    Returns:
        List of paths to extracted files
    """
    gz_path = Path(gz_dir)
    output_path = Path(output_dir)
    
    # Create output directory
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Find .grib2.gz files
    gz_files = list(gz_path.glob("*.grib2.gz"))
    if not gz_files:
        print(f"No .grib2.gz files found in {gz_path}")
        return []
    
    print(f"Found {len(gz_files)} .grib2.gz files")
    
    extracted_files = []
    
    for i, gz_file in enumerate(gz_files, 1):
        # Output filename (remove .gz)
        output_file = output_path / gz_file.stem
        
        print(f"[{i}/{len(gz_files)}] Extracting: {gz_file.name}")
        
        try:
            with gzip.open(gz_file, 'rb') as f_in:
                with open(output_file, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            
            size_mb = output_file.stat().st_size / (1024*1024)
            print(f"     → {output_file.name} ({size_mb:.1f} MB)")
            extracted_files.append(output_file)
            
        except Exception as e:
            print(f"     ❌ Error: {e}")
    
    print(f"\n✅ Extracted {len(extracted_files)} files to {output_path}")
    return extracted_files

if __name__ == "__main__":
    # Can run this module independently
    if len(sys.argv) == 3:
        extract_grib_files(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python extractor.py <gz_dir> <output_dir>")