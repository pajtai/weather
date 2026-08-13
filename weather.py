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
            country = res.get("country_code", "")
            location_label = ", ".join(filter(None, [city, state, country]))
            return res["latitude"], res["longitude"], location_label
    except Exception:
        pass
    return None

def get_location_by_ip():
    """Detect local coordinates via IP geolocation."""
    try:
        req = urllib.request.urlopen("http://ip-api.com/json/", timeout=3)
        data = json.loads(req.read().decode())
        if data.get("status") == "success":
            return data["lat"], data["lon"], f"{data['city']}, {data['country']}"
    except Exception:
        pass
    return 37.7749, -122.4194, "San Francisco, US (Default)"

def get_location():
    """Determine coordinates based on terminal input or IP fallback."""
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        coords = get_location_by_name(query)
        if coords:
            return coords
        print(f"⚠️ Couldn't find '{query}'. Falling back to IP location...\n")
    
    return get_location_by_ip()

def fetch_forecast(lat, lon):
    """Fetch 10-day forecast data."""
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}&"
        f"daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum&"
        f"forecast_days=10&timezone=auto"
    )
    req = urllib.request.urlopen(url, timeout=5, context=SSL_CONTEXT)
    return json.loads(req.read().decode())

def display_forecast():
    lat, lon, location = get_location()
    data = fetch_forecast(lat, lon)
    daily = data["daily"]
    unit_temp = data["daily_units"]["temperature_2m_max"]
    unit_precip = data["daily_units"]["precipitation_sum"]

    print(f"\n🌍 10-Day Weather Forecast: {location}")
    print("=" * 68)
    print(f"{'Date':<12} | {'Condition':<22} | {'High / Low':<14} | {'Precip':<8}")
    print("-" * 68)

    for i in range(len(daily["time"])):
        date_formatted = datetime.strptime(daily["time"][i], "%Y-%m-%d").strftime("%a, %b %d")
        code = daily["weather_code"][i]
        icon, desc = WEATHER_CODES.get(code, ("❓ ", "Unknown"))
        
        t_max = daily["temperature_2m_max"][i]
        t_min = daily["temperature_2m_min"][i]
        precip = daily["precipitation_sum"][i]

        condition_str = f"{icon} {desc}"
        temp_str = f"{t_max:.1f}° / {t_min:.1f}°{unit_temp}"
        precip_str = f"{precip:.1f} {unit_precip}"

        print(f"{date_formatted:<12} | {condition_str:<22} | {temp_str:<14} | {precip_str:<8}")

    print("=" * 68 + "\n")

if __name__ == "__main__":
    display_forecast()
