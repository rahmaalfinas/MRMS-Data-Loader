# main.py
"""
Main entry point for MRMS data processing.
Run individual modules or the full pipeline.
"""
import sys
from pathlib import Path

def show_usage():
    """Show usage instructions."""
    print("MRMS Data Processor")
    print("=" * 40)
    print("Usage:")
    print("  python main.py [command]")
    print("\nCommands:")
    print("  analyze     - Analyze data and show patch locations")
    print("  process     - Run full pipeline (analyze + crop)")
    print("  extract     - Extract .grib2.gz files only")
    print("  crop        - Crop patches only (requires analysis first)")
    print("  help        - Show this help")

def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        show_usage()
        return
    
    command = sys.argv[1].lower()
    
    try:
        if command == "analyze":
            from scripts.analyzer_cli import run_analysis
            run_analysis()
        
        elif command == "process":
            from scripts.analyzer_cli import run_analysis
            from scripts.cropper_cli import run_cropping

            """Run the full pipeline: analyze → confirm → crop."""
            print("Running Full Pipeline")
            print("=" * 50)
            run_analysis()
            run_cropping()
            print("\n✅ Pipeline complete!")
        
        elif command == "extract":
            from scripts.extractor import extract_grib_files
            from scripts.config import COMPRESSED_DIR, RAW_DATA_DIR
            extract_grib_files(COMPRESSED_DIR, RAW_DATA_DIR)
        
        elif command == "crop":
            from scripts.cropper_cli import run_cropping
            run_cropping()
        
        elif command == "help":
            show_usage()
        
        else:
            print(f"Unknown command: {command}")
            show_usage()

    except ImportError as e:
        print(f"Error: Missing required module or script. {e}")
        print("Ensure you are running from the project root directory.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# --- THIS IS THE PART YOU WERE MISSING ---
if __name__ == "__main__":
    main()