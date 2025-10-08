# OpenWeatherMap MCP Server

MCP server for accessing comprehensive weather data from OpenWeatherMap. Get current weather, forecasts, alerts, air quality, UV index, and historical data for 200,000+ cities worldwide.

## Features

- **Current Weather**: Real-time weather conditions for any location
- **Forecasts**: 5-day forecast with 3-hour intervals, hourly forecasts
- **Weather Alerts**: Severe weather warnings and alerts
- **Air Quality**: AQI and pollutant measurements (PM2.5, PM10, O3, NO2, SO2, CO)
- **Historical Data**: Access past weather data
- **UV Index**: Current UV radiation levels
- **City Search**: Search and geocode city names
- **Multiple Units**: Support for metric, imperial, and standard units

## Setup

### Prerequisites

- OpenWeatherMap account
- API key from [openweathermap.org](https://openweathermap.org/api)

### Environment Variables

- `OPENWEATHERMAP_API_KEY` (required): Your OpenWeatherMap API key

**How to get an API key:**
1. Go to [openweathermap.org/api](https://openweathermap.org/api)
2. Sign up for a free or paid account
3. Navigate to API keys section in your account
4. Generate and copy your API key
5. Free tier includes 1,000 calls/day and 60 calls/minute

## Available Tools

### Current Weather Tools

#### `get_current_weather`
Get current weather conditions for a location.

**Parameters:**
- `city` (string, optional): City name (e.g., 'London', 'New York,US', 'Tokyo,JP')
- `lat` (float, optional): Latitude coordinate (use with lon)
- `lon` (float, optional): Longitude coordinate (use with lat)
- `units` (string, optional): Units ('metric', 'imperial', 'standard', default: 'metric')

**Note:** Provide either city name OR coordinates, not both.

**Example:**
```python
# By city name
weather = await get_current_weather(
    city="London,GB",
    units="metric"
)

# By coordinates
weather = await get_current_weather(
    lat=51.5074,
    lon=-0.1278,
    units="metric"
)
```

**Response includes:**
- Temperature (current, feels like, min, max)
- Humidity, pressure, visibility
- Wind speed and direction
- Cloud coverage
- Weather conditions and description
- Sunrise and sunset times

#### `get_weather_by_zip`
Get current weather by ZIP or postal code.

**Parameters:**
- `zip_code` (string, required): ZIP or postal code
- `country_code` (string, optional): 2-letter country code (e.g., 'US', 'GB', 'CA')
- `units` (string, optional): Units (default: 'metric')

**Example:**
```python
weather = await get_weather_by_zip(
    zip_code="10001",
    country_code="US",
    units="imperial"
)
```

### Forecast Tools

#### `get_forecast`
Get 5-day weather forecast with 3-hour intervals (up to 40 data points).

**Parameters:**
- `city` (string, optional): City name
- `lat` (float, optional): Latitude (use with lon)
- `lon` (float, optional): Longitude (use with lat)
- `units` (string, optional): Units (default: 'metric')
- `cnt` (int, optional): Number of timestamps to return (max: 40)

**Example:**
```python
forecast = await get_forecast(
    city="Paris,FR",
    units="metric",
    cnt=10  # Get next 30 hours (10 x 3-hour intervals)
)
```

**Response includes:**
- 5-day forecast data
- 3-hour interval predictions
- Temperature, precipitation, wind, clouds
- Weather conditions for each timestamp

#### `get_hourly_forecast`
Get hourly weather forecast for 48 hours.

**Parameters:**
- `lat` (float, required): Latitude coordinate
- `lon` (float, required): Longitude coordinate
- `units` (string, optional): Units (default: 'metric')
- `cnt` (int, optional): Number of hours (max: 96)

**Example:**
```python
hourly = await get_hourly_forecast(
    lat=40.7128,
    lon=-74.0060,
    units="imperial",
    cnt=24  # Next 24 hours
)
```

### Weather Alerts Tools

#### `get_weather_alerts`
Get severe weather alerts and warnings for a location.

**Parameters:**
- `lat` (float, required): Latitude coordinate
- `lon` (float, required): Longitude coordinate

**Example:**
```python
alerts = await get_weather_alerts(
    lat=25.7617,
    lon=-80.1918  # Miami, FL
)
```

**Response includes:**
- Active weather alerts
- Severity levels
- Event type (e.g., hurricane, tornado, flood)
- Start and end times
- Description and instructions

### Air Quality Tools

#### `get_air_quality`
Get air quality index and pollutant concentrations.

**Parameters:**
- `lat` (float, required): Latitude coordinate
- `lon` (float, required): Longitude coordinate

**Example:**
```python
aqi = await get_air_quality(
    lat=35.6762,
    lon=139.6503  # Tokyo
)
```

**Response includes:**
- Air Quality Index (AQI): 1 (Good) to 5 (Very Poor)
- Pollutant concentrations:
  - CO (Carbon monoxide, μg/m³)
  - NO (Nitrogen monoxide, μg/m³)
  - NO2 (Nitrogen dioxide, μg/m³)
  - O3 (Ozone, μg/m³)
  - SO2 (Sulphur dioxide, μg/m³)
  - PM2.5 (Fine particles, μg/m³)
  - PM10 (Coarse particles, μg/m³)
  - NH3 (Ammonia, μg/m³)

### Location Tools

#### `search_city`
Search for cities by name and get their coordinates.

**Parameters:**
- `city_name` (string, required): City name to search
- `limit` (int, optional): Number of results (max: 5, default: 5)

**Example:**
```python
cities = await search_city(
    city_name="Springfield",
    limit=5
)
```

**Response includes:**
- City name
- Country code
- State (if applicable)
- Latitude and longitude
- Multiple matches for ambiguous names

### Historical & UV Tools

#### `get_historical_weather`
Get historical weather data for a specific date (last 5 days).

**Parameters:**
- `lat` (float, required): Latitude coordinate
- `lon` (float, required): Longitude coordinate
- `dt` (int, required): Unix timestamp (UTC) for the date
- `units` (string, optional): Units (default: 'metric')

**Example:**
```python
import time

# Get weather from 3 days ago
three_days_ago = int(time.time()) - (3 * 24 * 60 * 60)

historical = await get_historical_weather(
    lat=48.8566,
    lon=2.3522,  # Paris
    dt=three_days_ago,
    units="metric"
)
```

#### `get_uv_index`
Get UV index for a location.

**Parameters:**
- `lat` (float, required): Latitude coordinate
- `lon` (float, required): Longitude coordinate

**Example:**
```python
uv = await get_uv_index(
    lat=34.0522,
    lon=-118.2437  # Los Angeles
)
```

**UV Index Scale:**
- 0-2: Low
- 3-5: Moderate
- 6-7: High
- 8-10: Very High
- 11+: Extreme

#### `get_weather_map`
Get weather map layer tile URL for visualizations.

**Parameters:**
- `layer` (string, required): Layer type ('temp_new', 'precipitation_new', 'clouds_new', 'pressure_new', 'wind_new')
- `z` (int, required): Zoom level (0-15)
- `x` (int, required): Tile X coordinate
- `y` (int, required): Tile Y coordinate

**Example:**
```python
map_tile = await get_weather_map(
    layer="temp_new",
    z=1,
    x=1,
    y=0
)
# Use map_tile['tile_url'] to fetch the image
```

## Units of Measurement

### Metric (default)
- Temperature: Celsius
- Wind speed: meter/sec
- Pressure: hPa
- Visibility: meters

### Imperial
- Temperature: Fahrenheit
- Wind speed: miles/hour
- Pressure: hPa
- Visibility: meters

### Standard (Kelvin)
- Temperature: Kelvin
- Wind speed: meter/sec
- Pressure: hPa
- Visibility: meters

## Coverage

- **Cities**: 200,000+ cities worldwide
- **Countries**: All countries
- **Languages**: 40+ languages for city names
- **Update Frequency**: Every 10 minutes for most locations
- **Historical Data**: Up to 40 years (paid plans)

## Rate Limits and Pricing

### Free Tier
- **1,000 calls/day**
- **60 calls/minute**
- Current weather and 5-day forecast
- Basic historical data (5 days)
- Air pollution data

### Startup Plan ($40/month)
- 100,000 calls/month
- 600 calls/minute
- 16-day daily forecast
- 5-day 3-hour forecast
- Weather alerts

### Developer Plan ($120/month)
- 300,000 calls/month
- 1,000 calls/minute
- All Startup features
- 48-hour hourly forecast
- 4-day 1-hour forecast

### Professional Plan ($600/month)
- 1,000,000 calls/month
- 3,000 calls/minute
- All Developer features
- 30-year historical data
- Weather maps

### Enterprise (Custom pricing)
- Unlimited calls
- Custom rate limits
- Full historical archive (40+ years)
- Dedicated support
- SLA guarantees

Visit [openweathermap.org/price](https://openweathermap.org/price) for current rates.

## Weather Data Available

### Temperature
- Current temperature
- Feels like temperature
- Minimum and maximum temperature
- Temperature at different altitudes

### Atmospheric Conditions
- Atmospheric pressure (sea level and ground level)
- Humidity percentage
- Visibility distance
- Cloud coverage percentage

### Wind
- Wind speed
- Wind direction (degrees)
- Wind gust speed

### Precipitation
- Rain volume (last 1h, last 3h)
- Snow volume (last 1h, last 3h)
- Probability of precipitation

### Time Data
- Sunrise time
- Sunset time
- Timezone offset
- Data calculation time

## Error Handling

Common error codes:
- **401 Unauthorized**: Invalid API key
- **404 Not Found**: City/location not found
- **429 Too Many Requests**: Rate limit exceeded
- **500 Server Error**: OpenWeatherMap service issue

**Rate Limit Headers:**
- `X-RateLimit-Limit`: Total requests allowed
- `X-RateLimit-Remaining`: Requests remaining

## Best Practices

1. **Cache responses**: Weather data updates every 10 minutes
2. **Use coordinates**: More accurate than city names
3. **Batch requests**: Group multiple locations when possible
4. **Monitor limits**: Track your API usage daily
5. **Handle errors**: Implement retry logic with exponential backoff
6. **Use appropriate units**: Match user's location/preference

## City Name Format

When using city names:
- Format: `{city name},{country code}`
- Examples: `London,GB`, `New York,US`, `Tokyo,JP`
- State codes: `Springfield,IL,US` (for US cities)
- Use comma separation for accuracy

## Geocoding

To convert addresses or place names to coordinates:
1. Use `search_city` to find coordinates
2. Use coordinates for more accurate weather queries
3. Store coordinates for frequently accessed locations

## API Documentation

For detailed information about OpenWeatherMap API:
- [API Documentation](https://openweathermap.org/api)
- [Current Weather](https://openweathermap.org/current)
- [Forecast API](https://openweathermap.org/forecast5)
- [Air Pollution API](https://openweathermap.org/api/air-pollution)
- [Weather Alerts](https://openweathermap.org/api/one-call-3)
- [Historical Data](https://openweathermap.org/api/one-call-3#history)

## Use Cases

- **Weather Apps**: Build comprehensive weather applications
- **Travel Planning**: Check weather for destinations
- **Agriculture**: Monitor weather for farming decisions
- **Event Planning**: Plan outdoor events with weather data
- **Transportation**: Route planning based on weather
- **Energy Management**: Optimize energy based on weather
- **Insurance**: Weather data for claims processing
- **Research**: Climate and weather pattern analysis

## Support

- [OpenWeatherMap FAQ](https://openweathermap.org/faq)
- [API Support](https://openweathermap.org/api-support)
- [Community Forum](https://openweathermap.org/community)
