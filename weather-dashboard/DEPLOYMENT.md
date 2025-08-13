# 🚀 Deployment Guide for Isengard

## Pre-Deployment Checklist

### 1. Get Weather API Key
- Sign up at [OpenWeatherMap](https://openweathermap.org/api)
- Get your free API key
- Keep it handy for environment variable setup

### 2. Project Files Ready ✅
- `app.py` - Main Flask application
- `state_data.py` - US states data
- `templates/index.html` - Frontend interface
- `requirements.txt` - Python dependencies
- `Procfile` - Process configuration
- `runtime.txt` - Python version specification

## Deployment Steps for Isengard

### Option 1: Using AWS App Runner (Recommended)

1. **Prepare Repository**
   ```bash
   # Initialize git if not already done
   git init
   git add .
   git commit -m "Initial commit - US Weather Dashboard"
   
   # Push to GitHub/CodeCommit
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **Deploy via App Runner**
   - Go to AWS App Runner in your Isengard account
   - Create new service from source code
   - Connect your repository
   - Configure build settings:
     - Build command: `pip install -r requirements.txt`
     - Start command: `gunicorn app:app --bind 0.0.0.0:$PORT`

3. **Environment Variables**
   Set in App Runner configuration:
   ```
   WEATHER_API_KEY=your_actual_api_key_here
   PORT=8000
   ```

### Option 2: Using AWS Elastic Beanstalk

1. **Install EB CLI**
   ```bash
   pip install awsebcli
   ```

2. **Initialize and Deploy**
   ```bash
   eb init
   # Select your region and application name
   
   eb create weather-dashboard
   # This creates and deploys your application
   ```

3. **Set Environment Variables**
   ```bash
   eb setenv WEATHER_API_KEY=your_actual_api_key_here
   ```

### Option 3: Using AWS Lambda + API Gateway

1. **Install Serverless Framework**
   ```bash
   npm install -g serverless
   npm install serverless-wsgi serverless-python-requirements
   ```

2. **Create serverless.yml** (I'll create this file)

3. **Deploy**
   ```bash
   serverless deploy
   ```

## Post-Deployment

1. **Test the Application**
   - Visit your deployed URL
   - Test state/city selection
   - Verify weather data loads
   - Check 7-day forecast functionality

2. **Monitor Performance**
   - Check CloudWatch logs
   - Monitor API usage
   - Set up alarms if needed

## Troubleshooting

### Common Issues:
- **API Key Error**: Ensure WEATHER_API_KEY is set correctly
- **Port Issues**: Make sure PORT environment variable is configured
- **Import Errors**: Verify all files are uploaded including state_data.py

### Logs:
- Check application logs in your chosen service
- Look for Python import errors or API connection issues

## Security Notes

- Never commit your actual API key to version control
- Use environment variables for all sensitive data
- Consider setting up API rate limiting
- Enable HTTPS in production

## Account Details
- **Isengard Account**: ibejalon+a2c@amazon.com
- **Recommended Service**: AWS App Runner (easiest) or Elastic Beanstalk
- **Region**: Choose closest to your users (us-east-1 or us-west-2)

## Support
If you encounter issues:
1. Check CloudWatch logs
2. Verify environment variables
3. Test API key with curl/Postman
4. Check security groups and networking