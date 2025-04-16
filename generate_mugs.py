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

def read_template(template_path):
    """Read the SVG template file."""
    with open(template_path, 'r') as file:
        return file.read()

def read_names(names_path):
    """Read the list of names from a text file, one name per line."""
    with open(names_path, 'r') as file:
        # Strip whitespace and filter out empty lines
        return [line.strip() for line in file if line.strip()]

def generate_mug_svg(template, name, output_path, veogo):
    """Generate a personalized mug by replacing the placeholder with a name."""
    template = re.sub(r'EMPLOYEENAME', f'{name}', template)
    
    template = template.split("[[[VEOGO]]]")
    if not veogo:
        template = template[0] + template[2]
    else:
        template = "".join(template)

    assert(not r'EMPLOYEENAME' in template)
    # Save to output file
    with open(output_path, 'w') as file:
        file.write(template)
    
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
    # Check if Inkscape is installed
    try:
        subprocess.run(["inkscape", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: Inkscape must be installed and accessible in your PATH to convert SVG to PDF.")
        print("Please install Inkscape or ensure it's in your system PATH.")
        return

    # Create output directory if it doesn't exist
    outfolder = "out"
    os.makedirs(outfolder, exist_ok=True)
    
    template = read_template("mug.svg")
    names = read_names("names.txt")
    
    # Count successful conversions
    success_count = 0
    
    # Generate a personalized PDF for each name and place in 
    
    for i, name in enumerate(names, 1):
        veogo = False
        if name[0] == "*":
            veogo = True
            name = name[1:]
        
        safe_name = "".join(c if c.isalnum() or c in [' ', '_', '-'] else '_' for c in name)
        safe_name = safe_name.replace(' ', '_')
            
        
        svg_file = Path(outfolder) / f"mug_{i:02d}_{safe_name}.svg"
        generate_mug_svg(template, name, svg_file, veogo)
        
        
        #png_file = str(svg_file).replace('mug', 'proof').replace('.svg', '.png')
        #
        #convert_svg_to_fmt(svg_file, png_file)
        #
        #generate_mug_svg(template, name, svg_file, context, veogo, True)
        #
        #pdf_file = str(svg_file).replace('mug', 'real').replace('.svg', '.pdf')
        #convert_svg_to_fmt(svg_file, pdf_file)
        


    """
    # Convert to PDF
    pdf_path = Path(args.output_dir) / f"{n}_mug_{i:02d}_{safe_name}.pdf"
    if convert_svg_to_pdf(svg_path, pdf_path):
        success_count += 1
        print(f"Generated: {pdf_path}")
    else:
        print(f"Failed to convert: {svg_path}")
    """
    #if removebg:personalized = re.sub(r'<rect style="fill:#000000;fill-opacity:1;stroke-width:0.213856" id="rect1" width="225.0" height="90.0" x="0" y="0" />', f'', personalized)
    

if __name__ == "__main__":
    main()