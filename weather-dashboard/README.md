# 🇺🇸 US States Weather Dashboard

A beautiful, real-time weather dashboard focused on all 50 US states. Built with Flask and vanilla JavaScript, perfect for testing cloud deployments!

## Features

- 🏛️ **50 US States** - Complete coverage of all US states with major cities
- 🌡️ **Real-time Weather** - Current temperature (°F), humidity, wind speed, pressure
- 📅 **7-Day Forecast** - Extended weather forecast with daily highs/lows and conditions
- 🕐 **Time Zones** - Local time display for each state's timezone
- 🌪️ **Tornado Risk** - Color-coded tornado likelihood by state
- 🌀 **Hurricane Risk** - Hurricane threat assessment with detailed info
- 🎯 **State Facts** - Nicknames, fun facts, and comprehensive state data
- 🗺️ **State Overview** - Weather for multiple cities with state info
- 🎲 **Random City** - Discover weather in a random US city
- 📊 **Search History** - Track your recent weather searches
- 📱 **Responsive Design** - Works great on mobile and desktop
- ☁️ **Cloud Ready** - Configured for easy deployment

## Quick Start

1. **Get a Weather API Key**
   - Sign up at [OpenWeatherMap](https://openweathermap.org/api)
   - Get your free API key

2. **Set Environment Variable**
   ```bash
   export WEATHER_API_KEY="your_actual_api_key_here"
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Locally**
   ```bash
   python app.py
   ```
   
   Visit `http://localhost:5000`

## Deployment to Isengard

1. **Set Environment Variables**
   ```bash
   # In your deployment environment
   WEATHER_API_KEY=your_actual_api_key_here
   PORT=5000
   ```

2. **Deploy**
   - The app includes `Procfile` and `runtime.txt` for easy deployment
   - Uses gunicorn for production serving
   - Health check endpoint at `/api/health`

## API Endpoints

- `GET /` - Main dashboard interface
- `GET /api/states` - Get all US states with their cities
- `GET /api/state-info/<state>` - Get comprehensive state information (timezone, risks, facts)
- `GET /api/weather/<state>/<city>` - Get weather with state-specific data
- `GET /api/forecast/<state>/<city>` - Get 7-day weather forecast for city
- `GET /api/weather/state/<state>` - Get weather overview with state facts
- `GET /api/history` - Get recent search history
- `GET /api/health` - Health check endpoint

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: Vanilla JavaScript + CSS
- **Weather Data**: OpenWeatherMap API
- **Production Server**: Gunicorn

## US-Specific Features

### 🕐 Time Zone Support
- Real-time local time for each state
- Handles complex zones like Arizona (no DST) and Indiana

### 🌪️ Tornado Risk Assessment
- **Very High**: Kansas, Oklahoma (Tornado Alley)
- **High**: Texas, Arkansas, Alabama, Illinois, Iowa, Missouri, Nebraska, Tennessee
- **Moderate**: Colorado, Georgia, Indiana, Kentucky, Louisiana, Michigan, Minnesota, Mississippi, North Carolina, North Dakota, Ohio, South Carolina, South Dakota, Wisconsin
- **Low**: Arizona, Connecticut, Delaware, Maryland, Massachusetts, Montana, New Hampshire, New Jersey, New Mexico, New York, Pennsylvania, Utah, Vermont, Virginia, West Virginia, Wyoming
- **Very Low**: Alaska, California, Hawaii, Maine, Nevada, Oregon, Rhode Island, Washington

### 🌀 Hurricane Risk Assessment
- **Very High**: Florida, Louisiana
- **High**: Hawaii, Mississippi, North Carolina, South Carolina, Texas
- **Moderate**: Alabama, Connecticut, Delaware, Georgia, Maine, Maryland, Massachusetts, New Hampshire, New Jersey, New York, Rhode Island, Virginia
- **Low**: Arkansas, California, Oregon, Pennsylvania, Vermont, West Virginia
- **Very Low**: All inland states

### 🎯 State Facts Database
- Official state nicknames
- Unique fun facts for each state
- Major cities and capitals
- Comprehensive timezone data

## Next Steps

Want to enhance this project? Try adding:
- Database storage (PostgreSQL/MongoDB)
- User authentication
- Weather forecasts (5-day)
- Severe weather alerts integration
- Historical weather data
- Data visualization charts
- National Weather Service API integration

Have fun testing in your Isengard account! 🚀