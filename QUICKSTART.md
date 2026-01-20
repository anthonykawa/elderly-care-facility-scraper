# Quick Start Guide - Standalone Executable

## For End Users (No Python Required)

### Download & Run

1. **Download** the `ElderlyCareScraper` executable for your operating system:
   - Windows: `ElderlyCareScraper.exe`
   - macOS: `ElderlyCareScraper` (macOS app)
   - Linux: `ElderlyCareScraper` (Linux binary)

2. **Run** the application:
   - **Windows**: Double-click `ElderlyCareScraper.exe`
   - **macOS**: Right-click → Open (first time only), then double-click
   - **Linux**: Double-click or run from terminal: `./ElderlyCareScraper`

3. **Use** the application:
   - Enter a California city name (e.g., "Los Angeles")
   - Click "Start Scraping"
   - Wait for the results
   - Find the CSV file in the same folder as the executable

### First Run Notes

#### Windows
- **Security Warning**: Windows Defender SmartScreen may show a warning
  - Click "More info" → "Run anyway"
  - This is normal for unsigned executables

#### macOS
- **Gatekeeper Security**: macOS may block the app
  - Right-click the app → "Open"
  - Click "Open" in the dialog
  - After first time, you can double-click normally

#### Linux
- **Make Executable**: If double-clicking doesn't work:
  ```bash
  chmod +x ElderlyCareScraper
  ./ElderlyCareScraper
  ```

### System Requirements

- **Internet Connection**: Required for scraping
- **Disk Space**: ~50 MB free space
- **Operating System**:
  - Windows 10 or later
  - macOS 10.14 (Mojave) or later
  - Linux with glibc 2.27 or later

### Troubleshooting

**Application won't start:**
- Ensure you have internet connection
- Try running from command line to see error messages
- Check that Chrome/Chromium can be installed automatically

**Chrome/ChromeDriver errors:**
- The app downloads ChromeDriver on first run
- Ensure you have ~200 MB free space for ChromeDriver
- Check firewall isn't blocking downloads

**CSV file not created:**
- Check the output log for errors
- Verify the city name is spelled correctly
- Some cities may have no facilities

### Support

For issues, check:
1. Output log in the application window
2. BUILD.md for detailed troubleshooting
3. README.md for general information

---

## For Developers

### Building Your Own Executable

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the build script:
   ```bash
   python build.py
   ```

3. Find the executable in `dist/` folder

See [BUILD.md](BUILD.md) for complete build instructions.
