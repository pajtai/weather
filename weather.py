#!/usr/bin/env python3
import json
import ssl
import sys
import urllib.parse
import urllib.request
from datetime import datetime

# Handle macOS SSL certificate verification
SSL_CONTEXT = ssl._create_unverified_context()

WEATHER_CODES = {
    0: ("☀️ ", "Clear sky"),
    1: ("🌤️ ", "Mainly clear"),
    2: ("⛅ ", "Partly cloudy"),
    3: ("☁️ ", "Overcast"),
    45: ("🌫️ ", "Foggy"),
    48: ("🌫️ ", "Depositing rime fog"),
    51: ("🌧️ ", "Light drizzle"),
    53: ("🌧️ ", "Moderate drizzle"),
    55: ("🌧️ ", "Dense drizzle"),
    61: ("🌧️ ", "Slight rain"),
    63: ("🌧️ ", "Moderate rain"),
    65: ("🌧️ ", "Heavy rain"),
    71: ("❄️ ", "Slight snow"),
    73: ("❄️ ", "Moderate snow"),
    75: ("❄️ ", "Heavy snow"),
    80: ("🌦️ ", "Slight showers"),
    81: ("🌦️ ", "Moderate showers"),
    82: ("⛈️ ", "Heavy showers"),
    95: ("🌩️ ", "Thunderstorm"),
}

def print_help():
    """Print command-line help instructions."""
    help_text = """
🌍 Weather Terminal App - Help Guide

USAGE:
  ./weather.py [options] [location]

FLAGS:
  -h, --help, help      Display this help menu
  -i, --imperial        Force imperial units (°F, inches)
  -m, --metric          Force metric units (°C, mm)

EXAMPLES:
  ./weather.py                       Auto-detect location & local units
  ./weather.py santa cruz            Searches Santa Cruz (US -> °F, in)
  ./weather.py berlin                Searches Berlin (Germany -> °C, mm)
  ./weather.py london --imperial     Searches London using °F and inches
  ./weather.py helpt                 Searches Helpt, Germany

FEATURES:
  • Auto-selects Imperial in the US and Metric elsewhere.
  • Manual override flags (--imperial / --metric).
  • Dynamic column widths and accurate terminal emoji alignment.
    """
    print(help_text)
    sys.exit(0)

def get_display_width(text):
    """Calculate true terminal display width, ignoring zero-width unicode modifiers."""
    clean = text.replace('\ufe0f', '')
    width = 0
    for char in clean:
        width += 2 if ord(char) > 0x2000 else 1
    return width

def pad_str(text, target_width):
    """Pad text with spaces based on its visual display width."""
    padding = max(0, target_width - get_display_width(text))
    return text + (" " * padding)

def get_location_by_name(query):
    """Convert city name to coordinates using Open-Meteo Geocoding."""
    encoded_query = urllib.parse.quote(query)
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={encoded_query}&count=1&language=en&format=json"
    try:
        req = urllib.request.urlopen(url, timeout=5, context=SSL_CONTEXT)
        data = json.loads(req.read().decode())
        if data.get("results"):
            res = data["results"][0]
            city = res.get("name", query)
            state = res.get("admin1", "")
            country_code = res.get("country_code", "")
            location_label = ", ".join(filter(None, [city, state, country_code]))
            return res["latitude"], res["longitude"], location_label, country_code
    except Exception:
        pass
    return None

def get_location_by_ip():
    """Detect local coordinates via IP geolocation."""
    try:
        req = urllib.request.urlopen("http://ip-api.com/json/", timeout=3)
        data = json.loads(req.read().decode())
        if data.get("status") == "success":
            country_code = data.get("countryCode", "")
            return data["lat"], data["lon"], f"{data['city']}, {data['country']}", country_code
    except Exception:
        pass
    return 37.7749, -122.4194, "San Francisco, US (Default)", "US"

def fetch_forecast(lat, lon, units):
    """Fetch 10-day forecast using specified units."""
    temp_unit = "fahrenheit" if units == "imperial" else "celsius"
    precip_unit = "inch" if units == "imperial" else "mm"

    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}&"
        f"daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max&"
        f"temperature_unit={temp_unit}&"
        f"precipitation_unit={precip_unit}&"
        f"forecast_days=10&timezone=auto"
    )
    req = urllib.request.urlopen(url, timeout=5, context=SSL_CONTEXT)
    return json.loads(req.read().decode())

def display_forecast():
    args = sys.argv[1:]
    unit_override = None
    query_parts = []

    # Parse command line flags
    for arg in args:
        arg_lower = arg.lower()
        if arg_lower in ["-h", "--help", "help"]:
            print_help()
        elif arg_lower in ["-i", "--imperial"]:
            unit_override = "imperial"
        elif arg_lower in ["-m", "--metric"]:
            unit_override = "metric"
        else:
            query_parts.append(arg)

    query = " ".join(query_parts).strip()

    # Determine location
    loc_info = None
    if query:
        loc_info = get_location_by_name(query)
        if not loc_info:
            print(f"⚠️ Couldn't find '{query}'. Falling back to IP location...\n")

    if not loc_info:
        loc_info = get_location_by_ip()

    lat, lon, location, country_code = loc_info

    # Determine units (Flag override > Country auto-detection)
    if unit_override:
        units = unit_override
    else:
        units = "imperial" if country_code.upper() == "US" else "metric"

    data = fetch_forecast(lat, lon, units)
    daily = data["daily"]
    unit_temp = data["daily_units"]["temperature_2m_max"]
    unit_precip = data["daily_units"]["precipitation_sum"]

    rows = []
    for i in range(len(daily["time"])):
        date_formatted = datetime.strptime(daily["time"][i], "%Y-%m-%d").strftime("%a, %b %d")
        code = daily["weather_code"][i]
        icon, desc = WEATHER_CODES.get(code, ("❓ ", "Unknown"))
        
        t_max = daily["temperature_2m_max"][i]
        t_min = daily["temperature_2m_min"][i]
        precip = daily["precipitation_sum"][i]
        prob = daily["precipitation_probability_max"][i]

        condition_str = f"{icon} {desc}"
        temp_str = f"{t_max:.1f}° / {t_min:.1f}{unit_temp}"
        
        # Format precipitation decimals based on unit
        precip_val = f"{precip:.2f}" if unit_precip == "inch" else f"{precip:.1f}"
        precip_str = f"{precip_val} {unit_precip} ({prob}%)"

        rows.append((date_formatted, condition_str, temp_str, precip_str))

    max_cond_width = max([get_display_width(r[1]) for r in rows] + [len("Condition")])
    table_width = 12 + 3 + max_cond_width + 3 + 15 + 3 + 18
    header_cond = pad_str("Condition", max_cond_width)

    print(f"\n🌍 10-Day Weather Forecast: {location}")
    print("=" * table_width)
    print(f"{'Date':<12} | {header_cond} | {'High / Low':<15} | {'Precip (Prob)':<18}")
    print("-" * table_width)

    for date_str, cond_str, temp_str, precip_str in rows:
        formatted_cond = pad_str(cond_str, max_cond_width)
        print(f"{date_str:<12} | {formatted_cond} | {temp_str:<15} | {precip_str:<18}")

    print("=" * table_width + "\n")

if __name__ == "__main__":
    display_forecast()
