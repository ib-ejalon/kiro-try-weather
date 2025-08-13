# 📋 Deployment Checklist for Isengard

## Before You Deploy

### ✅ Prerequisites
- [ ] OpenWeatherMap API key obtained
- [ ] AWS Isengard account access (ibejalon+a2c@amazon.com)
- [ ] Git repository ready (optional but recommended)

### ✅ Environment Setup
```bash
# 1. Set your API key
export WEATHER_API_KEY="your_actual_openweathermap_api_key"

# 2. Test locally (optional)
python test_app.py

# 3. Run local server to verify
python app.py
# Visit http://localhost:5000
```

## Deployment Options (Choose One)

### 🚀 Option 1: AWS App Runner (Easiest)

**Steps:**
1. Push code to GitHub/CodeCommit
2. AWS Console → App Runner → Create Service
3. Source: Repository
4. Configure:
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn app:app --bind 0.0.0.0:$PORT`
5. Environment variables:
   - `WEATHER_API_KEY`: your_api_key
   - `PORT`: 8000
6. Deploy!

**Pros:** Easiest, auto-scaling, managed
**Cons:** Slightly more expensive

### 🌱 Option 2: AWS Elastic Beanstalk

**Steps:**
```bash
# Install EB CLI
pip install awsebcli

# Deploy
./deploy.sh
# Choose option 2
```

**Pros:** Good balance of control and ease
**Cons:** Requires EB CLI setup

### ⚡ Option 3: AWS Lambda (Serverless)

**Steps:**
```bash
# Install Serverless Framework
npm install -g serverless

# Deploy
./deploy.sh
# Choose option 3
```

**Pros:** Pay per request, scales to zero
**Cons:** Cold starts, more complex

## Post-Deployment Testing

### ✅ Verify Functionality
- [ ] Main page loads
- [ ] State dropdown populates
- [ ] City selection works
- [ ] Current weather displays
- [ ] 7-day forecast works
- [ ] State facts load
- [ ] State overview functions
- [ ] Random city feature works

### ✅ Performance Check
- [ ] Page loads in < 3 seconds
- [ ] API responses are fast
- [ ] No console errors
- [ ] Mobile responsive

## Monitoring Setup

### ✅ CloudWatch (Recommended)
- [ ] Set up log monitoring
- [ ] Create error rate alarms
- [ ] Monitor API usage

### ✅ Health Checks
- [ ] Test `/api/health` endpoint
- [ ] Set up uptime monitoring

## Security Checklist

### ✅ Environment Variables
- [ ] API key not in source code
- [ ] Environment variables properly set
- [ ] No sensitive data in logs

### ✅ Network Security
- [ ] HTTPS enabled
- [ ] CORS configured if needed
- [ ] Rate limiting considered

## Troubleshooting Guide

### Common Issues:

**"Invalid API Key"**
- Check WEATHER_API_KEY environment variable
- Verify key is active on OpenWeatherMap

**"Module not found"**
- Ensure all files uploaded (especially state_data.py)
- Check requirements.txt is complete

**"Port binding error"**
- Verify PORT environment variable
- Check Procfile configuration

**Slow responses**
- Check API rate limits
- Consider caching implementation

## Success Metrics

Your deployment is successful when:
- ✅ All 50 states load correctly
- ✅ Weather data displays for major cities
- ✅ 7-day forecasts work
- ✅ State facts and risks show properly
- ✅ No console errors
- ✅ Mobile-friendly interface

## Next Steps After Deployment

1. **Share the URL** with stakeholders
2. **Monitor usage** in first 24 hours
3. **Set up alerts** for errors
4. **Consider enhancements**:
   - Weather alerts
   - Historical data
   - User favorites
   - Social sharing

## Support

If you need help:
1. Check CloudWatch logs
2. Test API key manually
3. Verify all environment variables
4. Check AWS service status

**Account**: ibejalon+a2c@amazon.com
**Recommended**: Start with App Runner for simplicity