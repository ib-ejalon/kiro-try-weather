from flask import Flask, render_template, request, jsonify
import requests
import json
from datetime import datetime, timedelta
import os
import pytz
from state_data import US_STATES_DATA, US_STATES

app = Flask(__name__)

# You'll need to get a free API key from openweathermap.org
WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY', 'your_api_key_here')
WEATHER_BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
FORECAST_BASE_URL = "http://api.openweathermap.org/data/2.5/forecast"

# Simple in-memory storage for demo (use a database in production)
weather_history = []

def get_risk_color(risk_level):
    """Return color code for risk levels"""
    colors = {
        'Very Low': '#2ecc71',
        'Low': '#f39c12', 
        'Moderate': '#e67e22',
        'High': '#e74c3c',
        'Very High': '#8e44ad'
    }
    return colors.get(risk_level, '#95a5a6')

def get_local_time(timezone_str):
    """Get current local time for a timezone"""
    try:
        tz = pytz.timezone(timezone_str)
        local_time = datetime.now(tz)
        return local_time.strftime('%I:%M %p %Z')
    except:
        return 'N/A'

def process_forecast_data(forecast_data):
    """Process 5-day forecast data into daily summaries"""
    daily_forecasts = {}
    
    for item in forecast_data['list']:
        # Convert timestamp to date
        dt = datetime.fromtimestamp(item['dt'])
        date_key = dt.strftime('%Y-%m-%d')
        
        if date_key not in daily_forecasts:
            daily_forecasts[date_key] = {
                'date': dt.strftime('%A, %b %d'),
                'temps': [],
                'descriptions': [],
                'icons': [],
                'humidity': [],
                'wind_speeds': []
            }
        
        daily_forecasts[date_key]['temps'].append(item['main']['temp'])
        daily_forecasts[date_key]['descriptions'].append(item['weather'][0]['description'])
        daily_forecasts[date_key]['icons'].append(item['weather'][0]['icon'])
        daily_forecasts[date_key]['humidity'].append(item['main']['humidity'])
        daily_forecasts[date_key]['wind_speeds'].append(item['wind']['speed'])
    
    # Process daily summaries
    processed_forecasts = []
    for date_key in sorted(daily_forecasts.keys())[:7]:  # Get 7 days
        day_data = daily_forecasts[date_key]
        
        # Calculate daily averages and pick most common description
        avg_temp = round(sum(day_data['temps']) / len(day_data['temps']))
        max_temp = round(max(day_data['temps']))
        min_temp = round(min(day_data['temps']))
        
        # Most common weather description and icon
        most_common_desc = max(set(day_data['descriptions']), key=day_data['descriptions'].count)
        most_common_icon = max(set(day_data['icons']), key=day_data['icons'].count)
        
        avg_humidity = round(sum(day_data['humidity']) / len(day_data['humidity']))
        avg_wind = round(sum(day_data['wind_speeds']) / len(day_data['wind_speeds']), 1)
        
        processed_forecasts.append({
            'date': day_data['date'],
            'avg_temp': avg_temp,
            'max_temp': max_temp,
            'min_temp': min_temp,
            'description': most_common_desc.title(),
            'icon': most_common_icon,
            'humidity': avg_humidity,
            'wind_speed': avg_wind
        })
    
    return processed_forecasts

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/states')
def get_states():
    return jsonify(US_STATES)

@app.route('/api/state-info/<state>')
def get_state_info(state):
    """Get comprehensive state information"""
    try:
        if state not in US_STATES_DATA:
            return jsonify({'error': 'Invalid state'}), 400
        
        state_info = US_STATES_DATA[state].copy()
        state_info['local_time'] = get_local_time(state_info['timezone'])
        state_info['tornado_color'] = get_risk_color(state_info['tornado_risk'])
        state_info['hurricane_color'] = get_risk_color(state_info['hurricane_risk'])
        
        return jsonify(state_info)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/weather/<state>/<city>')
def get_weather(state, city):
    try:
        # Validate state and city
        if state not in US_STATES_DATA:
            return jsonify({'error': 'Invalid state'}), 400
        
        if city not in US_STATES_DATA[state]['cities']:
            return jsonify({'error': f'City not found in {state}'}), 400
        
        # Add state to query for better accuracy
        query = f"{city},{state},US"
        
        params = {
            'q': query,
            'appid': WEATHER_API_KEY,
            'units': 'imperial'  # Using Fahrenheit for US
        }
        
        response = requests.get(WEATHER_BASE_URL, params=params)
        
        if response.status_code == 200:
            data = response.json()
            
            # Get state info
            state_data = US_STATES_DATA[state]
            
            weather_info = {
                'city': data['name'],
                'state': state,
                'country': data['sys']['country'],
                'temperature': round(data['main']['temp']),
                'feels_like': round(data['main']['feels_like']),
                'humidity': data['main']['humidity'],
                'description': data['weather'][0]['description'].title(),
                'icon': data['weather'][0]['icon'],
                'wind_speed': round(data['wind']['speed'], 1),
                'pressure': data['main']['pressure'],
                'visibility': data.get('visibility', 0) / 1000,  # Convert to miles
                'timestamp': datetime.now().isoformat(),
                # State-specific info
                'timezone': state_data['timezone'],
                'local_time': get_local_time(state_data['timezone']),
                'tornado_risk': state_data['tornado_risk'],
                'hurricane_risk': state_data['hurricane_risk'],
                'tornado_color': get_risk_color(state_data['tornado_risk']),
                'hurricane_color': get_risk_color(state_data['hurricane_risk']),
                'nickname': state_data['nickname'],
                'fun_fact': state_data['fun_fact']
            }
            
            # Store in history
            weather_history.append(weather_info)
            if len(weather_history) > 50:  # Keep last 50 entries
                weather_history.pop(0)
            
            return jsonify(weather_info)
        else:
            return jsonify({'error': 'Weather data not found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/weather/state/<state>')
def get_state_overview(state):
    """Get weather for all major cities in a state"""
    try:
        if state not in US_STATES_DATA:
            return jsonify({'error': 'Invalid state'}), 400
        
        cities_weather = []
        state_data = US_STATES_DATA[state]
        
        for city in state_data['cities'][:4]:  # Get first 4 cities
            try:
                query = f"{city},{state},US"
                params = {
                    'q': query,
                    'appid': WEATHER_API_KEY,
                    'units': 'imperial'
                }
                
                response = requests.get(WEATHER_BASE_URL, params=params)
                if response.status_code == 200:
                    data = response.json()
                    cities_weather.append({
                        'city': data['name'],
                        'temperature': round(data['main']['temp']),
                        'description': data['weather'][0]['description'].title(),
                        'icon': data['weather'][0]['icon']
                    })
            except:
                continue
        
        return jsonify({
            'state': state,
            'cities': cities_weather,
            'timestamp': datetime.now().isoformat(),
            'state_info': {
                'nickname': state_data['nickname'],
                'timezone': state_data['timezone'],
                'local_time': get_local_time(state_data['timezone']),
                'tornado_risk': state_data['tornado_risk'],
                'hurricane_risk': state_data['hurricane_risk'],
                'tornado_color': get_risk_color(state_data['tornado_risk']),
                'hurricane_color': get_risk_color(state_data['hurricane_risk']),
                'fun_fact': state_data['fun_fact']
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/forecast/<state>/<city>')
def get_forecast(state, city):
    """Get 7-day weather forecast for a city"""
    try:
        # Validate state and city
        if state not in US_STATES_DATA:
            return jsonify({'error': 'Invalid state'}), 400
        
        if city not in US_STATES_DATA[state]['cities']:
            return jsonify({'error': f'City not found in {state}'}), 400
        
        # Add state to query for better accuracy
        query = f"{city},{state},US"
        
        params = {
            'q': query,
            'appid': WEATHER_API_KEY,
            'units': 'imperial'
        }
        
        response = requests.get(FORECAST_BASE_URL, params=params)
        
        if response.status_code == 200:
            forecast_data = response.json()
            
            # Process the forecast data
            daily_forecasts = process_forecast_data(forecast_data)
            
            # Get state info
            state_data = US_STATES_DATA[state]
            
            return jsonify({
                'city': forecast_data['city']['name'],
                'state': state,
                'forecasts': daily_forecasts,
                'timezone': state_data['timezone'],
                'local_time': get_local_time(state_data['timezone']),
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({'error': 'Forecast data not found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/history')
def get_history():
    return jsonify(weather_history[-10:])  # Return last 10 searches

@app.route('/api/health')
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))