#!/usr/bin/env python3
"""
Build script to create executables for all platforms.
Run this script to build the executable for your current platform.
"""

import subprocess
import sys
import os
import platform

def build_executable():
    """Build the executable using PyInstaller."""
    
    print("=" * 60)
    print("Building Elderly Care Facility Scraper Executable")
    print("=" * 60)
    print(f"Platform: {platform.system()}")
    print(f"Python: {sys.version}")
    print()
    
    # Find chromedriver to bundle with the app
    chromedriver_path = None
    import shutil
    chromedriver_path = shutil.which('chromedriver')
    
    if not chromedriver_path:
        print("⚠ WARNING: chromedriver not found in PATH")
        print("The app may not work without chromedriver installed.")
        print("Install it with: brew install chromedriver")
        print()
    else:
        print(f"✓ Found chromedriver: {chromedriver_path}")
        print()
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",  # Create a single executable file
        "--windowed",  # No console window (GUI only)
        "--name=ElderlyCareScraper",  # Name of the executable
        "--add-data=scraper.py:.",  # Include the scraper module
        "--clean",  # Clean cache before building
        "scraper_gui.py"
    ]
    
    # Add chromedriver binary if found
    if chromedriver_path and platform.system() == "Darwin":
        cmd.insert(-1, f"--add-binary={chromedriver_path}:.")
    
    # On Windows, add icon if available
    if platform.system() == "Windows" and os.path.exists("icon.ico"):
        cmd.insert(2, "--icon=icon.ico")
    
    # On macOS, add icon if available
    if platform.system() == "Darwin" and os.path.exists("icon.icns"):
        cmd.insert(2, "--icon=icon.icns")
    
    print("Building executable...")
    print(f"Command: {' '.join(cmd)}")
    print()
    
    try:
        result = subprocess.run(cmd, check=True)
        print()
        print("=" * 60)
        print("✓ Build completed successfully!")
        print("=" * 60)
        print()
        print(f"Executable location: ./dist/ElderlyCareScraper{'.exe' if platform.system() == 'Windows' else ''}")
        print()
        print("You can now distribute the executable file from the 'dist' folder.")
        print("Users can double-click it to run the application.")
        
    except subprocess.CalledProcessError as e:
        print()
        print("=" * 60)
        print("✗ Build failed!")
        print("=" * 60)
        print(f"Error: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print()
        print("=" * 60)
        print("✗ PyInstaller not found!")
        print("=" * 60)
        print("Please install PyInstaller first:")
        print("  pip install pyinstaller")
        sys.exit(1)

if __name__ == "__main__":
    build_executable()
