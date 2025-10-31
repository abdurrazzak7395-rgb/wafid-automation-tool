# Wafid Medical Appointment Automation Tool

A comprehensive automation tool for booking medical examination appointments on wafid.com/book-appointment.

## Features

- **Proxy Management**: Automatic proxy IP fetching, testing, and rotation
- **Fresh Browser Sessions**: Clean sessions for each attempt
- **Real-time Logging**: Comprehensive logging system
- **GUI Interface**: User-friendly interface with live console
- **Smart Matching**: Automated medical center matching and retry logic
- **Data Export**: CSV templates and payment URL capture

## Project Structure

```
bot/
├── src/
│   ├── components/
│   │   ├── proxy_manager.py      # Proxy handling and validation
│   │   ├── browser_automation.py # Browser session management
│   │   ├── form_handler.py       # Form filling and submission
│   │   ├── network_monitor.py    # Network request/response monitoring
│   │   └── logger.py             # Real-time logging system
│   ├── gui/
│   │   └── main_window.py        # GUI interface
│   └── main.py                   # Main application entry point
├── data/
│   ├── demo_candidates.csv       # Demo CSV template
│   ├── working_proxies.json      # Validated proxy list
│   └── payment_urls.csv          # Captured payment URLs
├── logs/
│   ├── automation.log            # Main log file
│   └── network_logs.json         # Network debugging logs
└── requirements.txt              # Python dependencies
```

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Install Chrome/Chromium browser and ChromeDriver

3. Run the application:
```bash
python src/main.py
```

## Usage

### GUI Mode

1. Launch the GUI application: `python main.py`
2. **Configure booking URL** (if different from default)
3. Set your target medical center name
4. Load candidate data from CSV
5. Start automation
6. Monitor real-time logs
7. Export captured payment URLs

### CLI Mode

```bash
python main.py --url "https://your-booking-site.com" --target "Medical Center" --csv data.csv
```

### Configuration

The booking URL can be configured in three ways:
1. **config.json** (recommended) - Edit the `booking_url` field
2. **Command line** - Use `--url` parameter
3. **GUI** - Update URL in the Configuration tab

See [URL_CONFIGURATION.md](URL_CONFIGURATION.md) for detailed instructions.

## Important Notes

- Each automation loop uses a fresh browser session and new proxy
- Medical center assignment is always extracted from live server responses
- All browser data is cleared between attempts to ensure fresh sessions
- Comprehensive logging for debugging and monitoring