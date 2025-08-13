#!/usr/bin/env python3
"""
Test script for US Weather Dashboard
Run this before deployment to verify everything works
"""

import os
import sys
import requests
from app import app

def test_api_key():
    """Test if API key is configured"""
    api_key = os.environ.get('WEATHER_API_KEY')
    if not api_key or api_key == 'your_api_key_here':
        print("❌ WEATHER_API_KEY not configured")
        print("Please set: export WEATHER_API_KEY='your_actual_key'")
        return False
    
    print("✅ API key configured")
    return True

def test_openweather_api():
    """Test OpenWeatherMap API connection"""
    api_key = os.environ.get('WEATHER_API_KEY')
    test_url = f"http://api.openweathermap.org/data/2.5/weather?q=New York,NY,US&appid={api_key}&units=imperial"
    
    try:
        response = requests.get(test_url, timeout=10)
        if response.status_code == 200:
            print("✅ OpenWeatherMap API connection successful")
            return True
        else:
            print(f"❌ API Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API Connection failed: {e}")
        return False

def test_flask_app():
    """Test Flask app routes"""
    with app.test_client() as client:
        # Test main page
        response = client.get('/')
        if response.status_code == 200:
            print("✅ Main page loads successfully")
        else:
            print("❌ Main page failed to load")
            return False
        
        # Test states API
        response = client.get('/api/states')
        if response.status_code == 200:
            print("✅ States API working")
        else:
            print("❌ States API failed")
            return False
        
        # Test health check
        response = client.get('/api/health')
        if response.status_code == 200:
            print("✅ Health check working")
        else:
            print("❌ Health check failed")
            return False
    
    return True

def main():
    print("🧪 Testing US Weather Dashboard")
    print("=" * 40)
    
    tests_passed = 0
    total_tests = 3
    
    # Test 1: API Key
    if test_api_key():
        tests_passed += 1
    
    # Test 2: External API
    if test_openweather_api():
        tests_passed += 1
    
    # Test 3: Flask App
    if test_flask_app():
        tests_passed += 1
    
    print("\n" + "=" * 40)
    print(f"Tests passed: {tests_passed}/{total_tests}")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! Ready for deployment.")
        return True
    else:
        print("❌ Some tests failed. Please fix issues before deploying.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)