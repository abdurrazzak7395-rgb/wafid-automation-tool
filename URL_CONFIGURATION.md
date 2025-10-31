# URL Configuration Guide

The Wafid Automation Tool now supports configurable booking URLs, allowing you to use different booking endpoints.

## Configuration Methods

### Method 1: config.json (Recommended)

Edit the `config.json` file in the project root:

```json
{
  "automation": {
    "booking_url": "https://your-booking-site.com/appointment",
    "max_retries": 100,
    ...
  }
}
```

### Method 2: Command Line (CLI Mode)

Use the `--url` parameter when running in CLI mode:

```bash
python main.py --url "https://your-booking-site.com/appointment" --target "Medical Center" --csv data.csv
```

### Method 3: GUI (Runtime Configuration)

1. Launch the GUI: `python main.py`
2. Go to the "Configuration" tab
3. Find the "Booking URL" section at the top
4. Enter your booking URL
5. Click "Update URL"

## URL Requirements

✅ Must start with `http://` or `https://`  
✅ Should be a valid, accessible URL  
✅ Must point to the booking form page

## Examples

### Valid URLs:
```
https://wafid.com/book-appointment
https://booking.example.com/appointments
http://localhost:8000/book
https://medical-center.com/booking/form
```

### Invalid URLs:
```
wafid.com/book-appointment          ❌ Missing protocol
ftp://wafid.com/book                ❌ Wrong protocol
                                     ❌ Empty URL
```

## Default URL

If no URL is configured, the tool uses the default:
```
https://wafid.com/book-appointment
```

## Troubleshooting

### URL Not Accessible

If you get "URL not accessible" errors:

1. **Check the URL**: Verify it's correct and accessible in a browser
2. **Check Network**: Ensure you have internet connectivity
3. **Check Proxies**: The tool uses proxies which might be blocked
4. **Check Firewall**: Your firewall might be blocking the connection

### URL Configuration Not Working

1. **Restart the application** after changing config.json
2. **Check JSON syntax** in config.json (use a JSON validator)
3. **Check file permissions** on config.json
4. **Check logs** in `logs/automation.log` for error messages

## Programmatic Usage

```python
from components.automation_engine import AutomationEngine

# Initialize with custom config file
engine = AutomationEngine(config_file="custom_config.json")

# Or set URL programmatically
engine.set_booking_url("https://your-site.com/booking")

# Validate URL
if engine.set_booking_url("https://example.com"):
    print("URL set successfully")
else:
    print("Invalid URL")
```

## Security Notes

- ⚠️ Always use HTTPS URLs when possible
- ⚠️ Verify the URL is legitimate before using
- ⚠️ Don't share URLs containing sensitive tokens or credentials
- ⚠️ The tool logs the URL - ensure logs are kept secure

## Related Files

- `config.json` - Main configuration file
- `src/components/automation_engine.py` - URL loading and validation
- `main.py` - CLI URL parameter handling
- `src/gui/main_window.py` - GUI URL configuration

## Support

If the booking URL is not accessible or you need help configuring it:

1. Check the URL in a web browser first
2. Review the logs in `logs/automation.log`
3. Verify your network connection and proxy settings
4. Ensure the booking site is operational

## Example: Changing from Default URL

**Before** (config.json):
```json
{
  "automation": {
    "booking_url": "https://wafid.com/book-appointment",
    ...
  }
}
```

**After** (config.json):
```json
{
  "automation": {
    "booking_url": "https://new-booking-site.com/appointments",
    ...
  }
}
```

Then restart the application or use the GUI to update the URL at runtime.
