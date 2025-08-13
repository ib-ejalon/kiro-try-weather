# 🔒 Private AWS App Runner Deployment Guide

**Account**: ibejalon+a2c@amazon.com  
**Use Case**: Private weather dashboard (not public)

## Step-by-Step Deployment

### 1. Get Your OpenWeatherMap API Key
1. Go to https://openweathermap.org/api
2. Sign up for free account
3. Navigate to API Keys section
4. Copy your API key (keep it secure!)

### 2. Push Code to AWS CodeCommit (Private Repository)

Since this is for private use, we'll use AWS CodeCommit for security:

```bash
# Login to your Isengard account first
aws configure  # Use your Isengard credentials

# Create CodeCommit repository
aws codecommit create-repository --repository-name us-weather-dashboard --repository-description "Private US Weather Dashboard"

# Add CodeCommit as remote
git remote add origin https://git-codecommit.us-east-1.amazonaws.com/v1/repos/us-weather-dashboard

# Push code
git push -u origin main
```

### 3. Deploy with AWS App Runner

#### Option A: AWS Console (Recommended for first deployment)

1. **Login to AWS Console**
   - Use your Isengard account: ibejalon+a2c@amazon.com
   - Navigate to AWS App Runner service

2. **Create App Runner Service**
   - Click "Create service"
   - Source: "Repository"
   - Repository type: "AWS CodeCommit"
   - Select your repository: "us-weather-dashboard"
   - Branch: "main"

3. **Configure Build**
   - Build settings: "Use a configuration file"
   - Configuration file: "apprunner.yaml"

4. **Configure Service**
   - Service name: "us-weather-dashboard"
   - Virtual CPU: 0.25 vCPU
   - Virtual memory: 0.5 GB

5. **Environment Variables**
   Add these environment variables:
   ```
   WEATHER_API_KEY = your_actual_openweathermap_api_key
   PORT = 8000
   ```

6. **Security (Important for Private Use)**
   - Auto-scaling: Min 1, Max 3 instances
   - Health check: "/api/health"
   - Tags: Add "Environment=Private" and "Owner=ibejalon"

7. **Deploy**
   - Review settings
   - Click "Create & deploy"
   - Wait 5-10 minutes for deployment

#### Option B: AWS CLI (Advanced)

```bash
# Create apprunner service
aws apprunner create-service \
    --service-name us-weather-dashboard \
    --source-configuration '{
        "CodeRepository": {
            "RepositoryUrl": "https://git-codecommit.us-east-1.amazonaws.com/v1/repos/us-weather-dashboard",
            "SourceCodeVersion": {
                "Type": "BRANCH",
                "Value": "main"
            },
            "CodeConfiguration": {
                "ConfigurationSource": "CONFIGURATION_FILE"
            }
        },
        "AutoDeploymentsEnabled": true
    }' \
    --instance-configuration '{
        "Cpu": "0.25 vCPU",
        "Memory": "0.5 GB"
    }'

# Set environment variables
aws apprunner update-service \
    --service-arn <your-service-arn> \
    --source-configuration '{
        "CodeRepository": {
            "CodeConfiguration": {
                "CodeConfigurationValues": {
                    "Runtime": "PYTHON_3",
                    "BuildCommand": "pip install -r requirements.txt",
                    "StartCommand": "gunicorn app:app --bind 0.0.0.0:$PORT",
                    "RuntimeEnvironmentVariables": {
                        "WEATHER_API_KEY": "your_actual_api_key",
                        "PORT": "8000"
                    }
                }
            }
        }
    }'
```

### 4. Access Control (Private Use)

Since this is private, consider these security measures:

1. **VPC Configuration** (Optional but recommended)
   - Deploy App Runner in private VPC
   - Use VPC endpoints for enhanced security

2. **Access Control**
   - Note the App Runner URL (it will be unique and hard to guess)
   - Consider adding basic authentication if needed
   - Monitor access logs in CloudWatch

3. **Cost Management**
   - Set up billing alerts
   - Monitor usage in AWS Cost Explorer
   - App Runner pricing: ~$0.007/hour for 0.25 vCPU + request charges

### 5. Post-Deployment

1. **Test Your Application**
   - Visit the App Runner URL
   - Test all features:
     - State selection
     - Weather data
     - 7-day forecast
     - State facts

2. **Monitor Performance**
   - Check CloudWatch logs
   - Monitor response times
   - Set up error alerts

3. **Backup Strategy**
   - Your code is in CodeCommit (backed up)
   - No database to backup (stateless app)
   - Document your API key securely

## Estimated Costs (Private Use)

- **App Runner**: ~$5-15/month (depending on usage)
- **CodeCommit**: Free (up to 5 users)
- **CloudWatch**: ~$1-3/month for logs
- **OpenWeatherMap API**: Free (up to 1000 calls/day)

**Total**: ~$6-18/month for private weather dashboard

## Troubleshooting

### Common Issues:
1. **Build fails**: Check requirements.txt and Python version
2. **API errors**: Verify WEATHER_API_KEY is set correctly
3. **Slow responses**: Check API rate limits
4. **Access denied**: Verify IAM permissions for CodeCommit

### Support:
- Check CloudWatch logs in App Runner console
- Test API key manually: `curl "http://api.openweathermap.org/data/2.5/weather?q=New York&appid=YOUR_KEY"`

## Security Best Practices

1. ✅ Never commit API keys to Git
2. ✅ Use environment variables for secrets
3. ✅ Monitor access logs regularly
4. ✅ Keep dependencies updated
5. ✅ Use HTTPS (App Runner provides this automatically)

Your private weather dashboard will be accessible only via the unique App Runner URL, making it secure for personal use!