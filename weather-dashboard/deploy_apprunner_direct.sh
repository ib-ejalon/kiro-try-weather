#!/bin/bash

echo "🚀 Direct AWS App Runner Deployment"
echo "==================================="

# Check if API key is set
if [ -z "$WEATHER_API_KEY" ]; then
    echo "⚠️  WEATHER_API_KEY not set"
    read -p "Enter your OpenWeatherMap API key: " api_key
    export WEATHER_API_KEY="$api_key"
    echo "✅ API key set: $WEATHER_API_KEY"
fi

# Create deployment package
echo "📦 Creating deployment package..."
zip -r weather-dashboard.zip . -x "*.git*" "*.DS_Store*" "node_modules/*" ".vscode/*"

echo "✅ Deployment package created: weather-dashboard.zip"
echo ""
echo "🎯 Next Steps:"
echo "=============="
echo ""
echo "1. Go to AWS App Runner Console:"
echo "   https://console.aws.amazon.com/apprunner/home"
echo ""
echo "2. Click 'Create service'"
echo ""
echo "3. Choose 'Source code repository' → 'Browse'"
echo ""
echo "4. Upload the file: weather-dashboard.zip"
echo ""
echo "5. Configure the service:"
echo "   - Service name: us-weather-dashboard"
echo "   - Runtime: Python 3"
echo "   - Build command: pip install -r requirements.txt"
echo "   - Start command: gunicorn app:app --bind 0.0.0.0:\$PORT"
echo ""
echo "6. Set Environment Variables:"
echo "   - WEATHER_API_KEY = $WEATHER_API_KEY"
echo "   - PORT = 8000"
echo ""
echo "7. Configure instance:"
echo "   - CPU: 0.25 vCPU"
echo "   - Memory: 0.5 GB"
echo ""
echo "8. Click 'Create & deploy'"
echo ""
echo "🔒 Your private weather dashboard will be ready in 5-10 minutes!"
echo "📱 You'll get a unique URL that only you know about."
echo ""
echo "💡 Save your API key for future reference:"
echo "   WEATHER_API_KEY=$WEATHER_API_KEY"