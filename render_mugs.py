#!/usr/bin/env python3
"""
Mug Design Generator
-------------------
This script takes a master SVG template and generates individualized PDF files
by replacing a placeholder string with custom names.

Usage:
  python mug_generator.py --template template.svg --output-dir output --names names.txt
"""

import os
import argparse
import re
import subprocess
from pathlib import Path
import tempfile
import shutil

def convert_svg_to_fmt(svg_path, out_path):
    """Convert SVG to PDF using Inkscape command line interface."""
    # Try with newer Inkscape syntax (Inkscape 1.0+)
    cmd = ["inkscape", "--export-filename=" + str(out_path), str(svg_path)]
    print(" ".join(cmd))
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=True
    )

    return True


def main():
    svg_files = []
    
    folder_path = "out"
    # Check if the folder exists
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist")
        return svg_files
    
    # Loop through all files in the folder
    for filename in os.listdir(folder_path):
        # Check if the file has .svg extension
        if filename.lower().endswith('.svg'):
            file_path = os.path.join(folder_path, filename)
            svg_files.append(file_path)
            print(f"Found SVG file: {file_path}")
    
    
    for svg in svg_files:
        png = svg.replace(".svg", ".png").replace("mug", "preview")
        convert_svg_to_fmt(svg, png)
        box = """<rect
       style="fill:#000000;fill-opacity:1;stroke-width:0.213856"
       id="rect1"
       width="225.0"
       height="90.0"
       x="0"
       y="0" />"""
        svg_data = open(svg).read().replace(box,"")
        tmp = "/tmp/temp.svg"
        with open(tmp, "w") as f:
            f.write(svg_data)


        pdf = svg.replace(".svg", ".pdf").replace("mug", "final")
        convert_svg_to_fmt(tmp, pdf)

    print(f"Total SVG files found: {len(svg_files)}")
    
    
if __name__ == "__main__":
    main()