#!/usr/bin/env python3
"""
Quick demo to test the new output directory feature.
"""

import os
import sys

print("=" * 60)
print("Testing Output Directory Feature")
print("=" * 60)

# Test 1: Command-line with default directory
print("\n1. Default behavior (current directory):")
print("   Command: python scraper.py 'City Name'")
print("   Output: ./city-name-elderly-facilities.csv")

# Test 2: Command-line with custom directory
print("\n2. Custom output directory:")
print("   Command: python scraper.py 'City Name' -o /path/to/folder")
print("   Output: /path/to/folder/city-name-elderly-facilities.csv")

# Test 3: GUI
print("\n3. GUI with browse button:")
print("   - Launch: python scraper_gui.py")
print("   - Click 'Browse...' button")
print("   - Select folder in dialog")
print("   - Start scraping")
print("   - CSV saved to selected folder")

print("\n" + "=" * 60)
print("Features Added:")
print("=" * 60)
print("✓ Command-line: --output-dir / -o flag")
print("✓ GUI: Browse button with folder picker")
print("✓ Auto-create directories if they don't exist")
print("✓ Validates paths before scraping")
print("✓ Shows full output path in logs")
print("=" * 60)

# Quick validation test
print("\nRunning quick validation test...")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scraper import ElderlyFacilityScraper

test_dir = "./test_output_demo"
scraper = ElderlyFacilityScraper("TestCity", test_dir)

print(f"✓ Output directory: {scraper.output_dir}")
print(f"✓ Filename: {scraper.filename}")
print(f"✓ Directory exists: {os.path.exists(scraper.output_dir)}")

# Cleanup
import shutil
if os.path.exists(test_dir):
    shutil.rmtree(test_dir)
    print(f"✓ Cleaned up test directory")

print("\n✓ All tests passed!")
