#!/bin/bash

echo "🚀 Deploying WhatsApp Lead Assistant to Render..."

# Check if we're in the right directory
if [ ! -f "main_simple.py" ]; then
    echo "❌ Error: main_simple.py not found. Please run this script from the project root."
    exit 1
fi

# Check if git is clean
if [ -n "$(git status --porcelain)" ]; then
    echo "⚠️  Warning: You have uncommitted changes. Consider committing them first."
    read -p "Continue anyway? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Push to GitHub
echo "📤 Pushing to GitHub..."
git add .
git commit -m "Deploy to Render - $(date)"
git push origin main

echo "✅ Code pushed to GitHub!"
echo ""
echo "🎯 Next Steps:"
echo "1. Go to https://render.com"
echo "2. Sign up/Login with your GitHub account"
echo "3. Click 'New +' and select 'Web Service'"
echo "4. Connect your GitHub repository: amanraj3103/WhatsApp-lead-assistant"
echo "5. Configure the service:"
echo "   - Name: whatsapp-lead-assistant"
echo "   - Environment: Python"
echo "   - Build Command: pip install -r requirements.txt && mkdir -p logs && mkdir -p billing_data"
echo "   - Start Command: python main_simple.py"
echo "   - Plan: Free"
echo ""
echo "6. Add environment variables:"
echo "   - TWILIO_ACCOUNT_SID"
echo "   - TWILIO_AUTH_TOKEN"
echo "   - TWILIO_PHONE_NUMBER"
echo "   - HUBSPOT_API_KEY"
echo "   - HUBSPOT_PORTAL_ID"
echo "   - CALENDLY_API_KEY"
echo "   - CALENDLY_USER_URI"
echo "   - ENCRYPTION_KEY"
echo ""
echo "7. Click 'Create Web Service'"
echo ""
echo "🌐 Your app will be available at: https://whatsapp-lead-assistant.onrender.com"
echo "📱 Webhook URL: https://whatsapp-lead-assistant.onrender.com/webhook"
echo ""
echo "💡 After deployment, configure Twilio webhook to point to your Render URL!" 