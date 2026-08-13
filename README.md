# 🌍 Simple Python Weather Terminal App 

## USAGE:
- `./weather.py`                     Fetch forecast for your current IP location\
- `./weather.py <location>`          Fetch forecast for a specific city/locatio\n
- `./weather.py -h | help | --help`  Display the help menu\

## EXAMPLES:
  `./weather.py`                       (Uses IP geolocation)\
  `./weather.py santa cruz`            (Searches for Santa Cruz)\
  `./weather.py helpt`                 (Searches for Helpt, Germany)\
  `./weather.py help`                  (Displays the help menu)\

## FEATURES:
- 10-day weather forecast with max/min temperatures in Fahrenheit (°F).\
- Auto-adjusting condition column based on the longest weather string.\
- Precipitation totals with peak percentage probability.\
    
### EXAMPLE:

```
❯ ./weather.py gamboa

🌍 10-Day Weather Forecast: Gamboa, Rio de Janeiro, BR
========================================================================
Date         | Condition            | High / Low      | Precip (Prob)
------------------------------------------------------------------------
Thu, Aug 13  | ☁️  Overcast         | 80.9° / 65.9°F  | 0.0 mm (2%)
Fri, Aug 14  | 🌧️  Light drizzle    | 75.7° / 69.3°F  | 1.3 mm (45%)
Sat, Aug 15  | 🌧️  Moderate drizzle | 75.4° / 68.6°F  | 2.8 mm (82%)
Sun, Aug 16  | ☁️  Overcast         | 78.4° / 68.3°F  | 0.0 mm (6%)
Mon, Aug 17  | ☁️  Overcast         | 80.8° / 68.0°F  | 0.0 mm (0%)
Tue, Aug 18  | ☀️  Clear sky        | 80.3° / 66.1°F  | 0.0 mm (2%)
Wed, Aug 19  | 🌤️  Mainly clear     | 79.9° / 68.6°F  | 0.0 mm (2%)
Thu, Aug 20  | ☁️  Overcast         | 80.9° / 69.6°F  | 0.0 mm (0%)
Fri, Aug 21  | 🌧️  Light drizzle    | 81.2° / 70.1°F  | 1.0 mm (10%)
Sat, Aug 22  | 🌧️  Light drizzle    | 74.6° / 69.6°F  | 0.8 mm (23%)
========================================================================

❯ ./weather.py gamboa, panama

🌍 10-Day Weather Forecast: Gamboa, Provincia de Colón, PA
========================================================================
Date         | Condition            | High / Low      | Precip (Prob)
------------------------------------------------------------------------
Thu, Aug 13  | 🌩️  Thunderstorm     | 85.4° / 76.6°F  | 4.4 mm (92%)
Fri, Aug 14  | 🌩️  Thunderstorm     | 85.5° / 75.5°F  | 9.5 mm (100%)
Sat, Aug 15  | 🌩️  Thunderstorm     | 84.7° / 73.8°F  | 29.4 mm (100%)
Sun, Aug 16  | 🌩️  Thunderstorm     | 83.6° / 74.2°F  | 24.9 mm (100%)
Mon, Aug 17  | 🌦️  Slight showers   | 81.9° / 74.7°F  | 10.2 mm (99%)
Tue, Aug 18  | 🌦️  Slight showers   | 84.7° / 74.9°F  | 13.4 mm (89%)
Wed, Aug 19  | 🌩️  Thunderstorm     | 84.3° / 75.8°F  | 14.6 mm (93%)
Thu, Aug 20  | 🌩️  Thunderstorm     | 80.3° / 75.3°F  | 24.4 mm (100%)
Fri, Aug 21  | 🌧️  Moderate drizzle | 87.3° / 75.5°F  | 7.8 mm (93%)
Sat, Aug 22  | 🌧️  Light drizzle    | 84.3° / 74.2°F  | 4.2 mm (94%)
========================================================================
```
