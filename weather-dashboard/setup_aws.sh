#!/bin/bash

echo "🔒 Setting up Private AWS Deployment"
echo "===================================="

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI not found. Please install it first:"
    echo "   brew install awscli  # macOS"
    echo "   pip install awscli   # Python"
    exit 1
fi

echo "✅ AWS CLI found"

# Check AWS credentials
if ! aws sts get-caller-identity &> /dev/null; then
    echo "❌ AWS credentials not configured"
    echo "Please run: aws configure"
    echo "Use your Isengard account credentials"
    exit 1
fi

echo "✅ AWS credentials configured"

# Get current AWS identity
IDENTITY=$(aws sts get-caller-identity --query 'Account' --output text)
echo "📋 AWS Account: $IDENTITY"

# Check if API key is set
if [ -z "$WEATHER_API_KEY" ]; then
    echo "⚠️  WEATHER_API_KEY not set"
    read -p "Enter your OpenWeatherMap API key: " api_key
    export WEATHER_API_KEY="$api_key"
    echo "✅ API key set for this session"
    echo "💡 To make it permanent, add to your ~/.bashrc or ~/.zshrc:"
    echo "   export WEATHER_API_KEY='$api_key'"
fi

# Create CodeCommit repository
echo ""
echo "📦 Creating CodeCommit repository..."

REPO_NAME="us-weather-dashboard"
REPO_EXISTS=$(aws codecommit get-repository --repository-name $REPO_NAME 2>/dev/null)

if [ $? -eq 0 ]; then
    echo "✅ Repository already exists"
else
    aws codecommit create-repository \
        --repository-name $REPO_NAME \
        --repository-description "Private US Weather Dashboard" \
        --tags Environment=Private,Owner=ibejalon
    
    if [ $? -eq 0 ]; then
        echo "✅ CodeCommit repository created"
    else
        echo "❌ Failed to create repository"
        exit 1
    fi
fi

# Get repository URL
REPO_URL=$(aws codecommit get-repository --repository-name $REPO_NAME --query 'repositoryMetadata.cloneUrlHttp' --output text)
echo "📍 Repository URL: $REPO_URL"

# Add remote if not exists
if ! git remote get-url origin &> /dev/null; then
    git remote add origin $REPO_URL
    echo "✅ Added CodeCommit as origin"
else
    echo "✅ Git remote already configured"
fi

# Push to CodeCommit
echo ""
echo "📤 Pushing code to CodeCommit..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo "✅ Code pushed successfully"
else
    echo "❌ Failed to push code"
    echo "💡 You may need to configure Git credentials for CodeCommit"
    echo "   See: https://docs.aws.amazon.com/codecommit/latest/userguide/setting-up-gc.html"
    exit 1
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Go to AWS App Runner console"
echo "2. Create service from CodeCommit repository: $REPO_NAME"
echo "3. Set environment variable: WEATHER_API_KEY=$WEATHER_API_KEY"
echo "4. Deploy and test!"
echo ""
echo "📖 See PRIVATE_DEPLOYMENT_GUIDE.md for detailed instructions"