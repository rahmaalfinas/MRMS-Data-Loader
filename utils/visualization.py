# utils/visualization.py
"""
Visualization utilities for MRMS data.
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

def plot_storm_centers(data, centers, patch_size=1468, output_dir=None):
    """Plot storm centers on the data."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    im = ax.imshow(data, cmap='viridis', vmin=0, vmax=70, aspect='auto')
    
    half = patch_size // 2
    for i, (row, col) in enumerate(centers):
        # Draw patch boundary
        rect = plt.Rectangle((col-half, row-half), patch_size, patch_size,
                           fill=False, edgecolor='white', linewidth=2)
        ax.add_patch(rect)
        
        # Mark center
        ax.plot(col, row, 'ro', markersize=8)
        ax.text(col, row, f'{i+1}', color='white', fontsize=12,
                ha='center', va='center', fontweight='bold')
    
    plt.colorbar(im, label='Reflectivity (dBZ)')
    plt.title(f"Storm Centers ({len(centers)} locations)")
    plt.xlabel("Columns")
    plt.ylabel("Rows")
    plt.tight_layout()

    if output_dir.is_dir():
            save_path = output_dir / "storm_centers_plot.png"
        
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    print(f"✅ Plot saved to: {save_path}")

    plt.show()