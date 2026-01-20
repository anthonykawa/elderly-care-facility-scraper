# Build Instructions for Elderly Care Facility Scraper

This document explains how to create standalone executable files for Windows, macOS, and Linux.

## Prerequisites

1. Install Python 3.8 or higher
2. Install all dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Building the Executable

### Quick Build (All Platforms)

Simply run the build script:

```bash
python build.py
```

This will create an executable in the `dist/` folder for your current platform.

### Platform-Specific Instructions

#### Windows
1. Run the build script:
   ```cmd
   python build.py
   ```
2. Find the executable at: `dist/ElderlyCareScraper.exe`
3. Double-click to run!

**Note:** On first run, Windows Defender SmartScreen may show a warning. Click "More info" → "Run anyway". This is normal for unsigned executables.

#### macOS
1. Run the build script:
   ```bash
   python build.py
   ```
2. Find the executable at: `dist/ElderlyCareScraper`
3. On first run, you may need to right-click → "Open" to bypass Gatekeeper security.

#### Linux
1. Run the build script:
   ```bash
   python build.py
   ```
2. Find the executable at: `dist/ElderlyCareScraper`
3. Make it executable (if needed):
   ```bash
   chmod +x dist/ElderlyCareScraper
   ```
4. Double-click or run from terminal

## Manual Build (Advanced)

If you prefer to customize the build, use PyInstaller directly:

```bash
pyinstaller --onefile --windowed --name=ElderlyCareScraper --add-data="scraper.py:." scraper_gui.py
```

### Additional PyInstaller Options

- `--icon=icon.ico` - Add custom icon (Windows)
- `--icon=icon.icns` - Add custom icon (macOS)
- `--add-data="file:."` - Include additional files
- `--hidden-import=module` - Include modules not auto-detected
- `--noconsole` - Hide console window (Windows)

## Distribution

### Single File Distribution
The executable in `dist/` is completely standalone and can be distributed as-is. Users can:
1. Download the file
2. Double-click to run
3. No Python installation required!

### What Gets Included
- Python interpreter
- All required libraries (Selenium, webdriver-manager, etc.)
- Your application code
- ChromeDriver (downloaded automatically on first run)

### File Sizes
Expect the executable to be approximately:
- **Windows**: 80-120 MB
- **macOS**: 90-130 MB  
- **Linux**: 80-110 MB

This is normal as it includes the entire Python runtime and dependencies.

## Troubleshooting

### "Module not found" error when running executable
- Add the missing module with `--hidden-import=module_name`
- Example: `pyinstaller --hidden-import=selenium.webdriver ...`

### Executable is too large
- Use `--exclude-module` to remove unused modules
- Consider using UPX compression (built into PyInstaller)

### Application doesn't start
- Run from command line to see error messages:
  - Windows: `dist\ElderlyCareScraper.exe`
  - macOS/Linux: `./dist/ElderlyCareScraper`

### Chrome/ChromeDriver issues
- The executable downloads ChromeDriver on first run
- Ensure internet connection is available
- ChromeDriver is cached for future use

## Creating Installers (Optional)

For a more professional distribution:

### Windows
Use **Inno Setup** or **NSIS** to create an installer:
```bash
# Install Inno Setup, then create a .iss script
# Example available at: https://jrsoftware.org/isinfo.php
```

### macOS
Create a .app bundle or .dmg:
```bash
# Use create-dmg or manually with hdiutil
```

### Linux
Create a .deb or .rpm package:
```bash
# Use fpm or native packaging tools
```

## Testing

Before distributing:
1. Test the executable on a clean machine (no Python installed)
2. Verify all features work correctly
3. Test with different cities
4. Check CSV file creation and contents

## Support

For issues with:
- Building: Check PyInstaller documentation
- Scraping: Review scraper.py logs
- GUI: Test scraper_gui.py directly first
