#!/bin/bash

echo "🚀 US Weather Dashboard Deployment Script"
echo "=========================================="

# Check if API key is set
if [ -z "$WEATHER_API_KEY" ]; then
    echo "❌ Error: WEATHER_API_KEY environment variable not set"
    echo "Please run: export WEATHER_API_KEY='your_api_key_here'"
    exit 1
fi

echo "✅ API key found"

# Check deployment method
echo ""
echo "Choose deployment method:"
echo "1) AWS App Runner (Recommended)"
echo "2) AWS Elastic Beanstalk"
echo "3) AWS Lambda (Serverless)"
echo "4) Local testing"

read -p "Enter choice (1-4): " choice

case $choice in
    1)
        echo "📋 App Runner deployment steps:"
        echo "1. Push code to GitHub/CodeCommit"
        echo "2. Go to AWS App Runner console"
        echo "3. Create service from source code"
        echo "4. Set WEATHER_API_KEY in environment variables"
        echo "5. Deploy!"
        ;;
    2)
        echo "🌱 Deploying with Elastic Beanstalk..."
        if ! command -v eb &> /dev/null; then
            echo "Installing EB CLI..."
            pip install awsebcli
        fi
        
        if [ ! -f ".elasticbeanstalk/config.yml" ]; then
            echo "Initializing EB application..."
            eb init --platform python-3.11 us-weather-dashboard
        fi
        
        echo "Creating/updating environment..."
        eb create weather-dashboard-env || eb deploy
        
        echo "Setting environment variables..."
        eb setenv WEATHER_API_KEY=$WEATHER_API_KEY
        
        echo "✅ Deployment complete!"
        eb open
        ;;
    3)
        echo "⚡ Deploying with Serverless..."
        if ! command -v serverless &> /dev/null; then
            echo "Please install Serverless Framework:"
            echo "npm install -g serverless"
            exit 1
        fi
        
        echo "Deploying to Lambda..."
        serverless deploy
        
        echo "✅ Serverless deployment complete!"
        ;;
    4)
        echo "🧪 Starting local development server..."
        echo "Installing dependencies..."
        pip install -r requirements.txt
        
        echo "Starting Flask app..."
        python app.py
        ;;
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "🎉 Deployment process initiated!"
echo "Don't forget to test your application after deployment."