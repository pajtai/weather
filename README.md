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
```

