# Elderly Care Facility Scraper

A tool to search for elderly care facilities in California cities and export the results to CSV. Available in both command-line and GUI versions.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### GUI Version (Recommended)

Launch the graphical user interface:

```bash
python scraper_gui.py
```

The GUI provides:
- Simple text input for city name
- Start/Stop buttons
- Real-time progress updates
- Output log viewer
- Cross-platform support (Windows, macOS, Linux)

### Command-Line Version

```bash
python scraper.py <city_name>
```

Example:
```bash
python scraper.py "Los Angeles"
```

This will create a CSV file named `los-angeles-elderly-facilities.csv` with the facility details.

## Creating Standalone Executables

Want to distribute the app without requiring Python? Create a standalone executable:

```bash
python build.py
```

This creates a double-clickable executable in the `dist/` folder that works without Python installed.

See [BUILD.md](BUILD.md) for detailed instructions on creating executables for Windows, macOS, and Linux.

## Output Format

The CSV file contains the following columns:
- Name
- Status
- Address
- Phone Number
- Facility Capacity

## Features

- ✅ Scrapes elderly care facilities from California's CCLD website
- ✅ Handles pagination automatically
- ✅ Saves data progressively (after each page)
- ✅ Interruption-safe (partial data is preserved)
- ✅ Cross-platform GUI application
- ✅ Real-time progress tracking
- ✅ Create standalone executables for distribution
