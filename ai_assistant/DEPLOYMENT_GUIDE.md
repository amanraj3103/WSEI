# 🚀 Deployment Guide - WhatsApp Lead Assistant

## 🎯 **Quick Deployment to Render (Recommended)**

### **Step 1: Prepare Your Code**
```bash
# Make sure all changes are committed
git add .
git commit -m "Ready for deployment"
git push origin main
```

### **Step 2: Deploy to Render**

1. **Go to Render.com**
   - Visit: https://render.com
   - Sign up/Login with your GitHub account

2. **Create New Web Service**
   - Click "New +" button
   - Select "Web Service"
   - Connect your GitHub repository: `amanraj3103/WhatsApp-lead-assistant`

3. **Configure the Service**
   ```
   Name: whatsapp-lead-assistant
   Environment: Python
   Region: Choose closest to your customers
   Branch: main
   Build Command: pip install -r requirements.txt && mkdir -p logs && mkdir -p billing_data
   Start Command: python main_simple.py
   Plan: Free (upgrade to $7/month Pro when you have customers)
   ```

4. **Add Environment Variables**
   Click "Environment" tab and add:
   ```
   TWILIO_ACCOUNT_SID=your_twilio_account_sid
   TWILIO_AUTH_TOKEN=your_twilio_auth_token
   TWILIO_PHONE_NUMBER=your_twilio_whatsapp_number
   HUBSPOT_API_KEY=your_hubspot_api_key
   HUBSPOT_PORTAL_ID=your_hubspot_portal_id
   CALENDLY_API_KEY=your_calendly_api_key
   CALENDLY_USER_URI=your_calendly_user_uri
   ENCRYPTION_KEY=your_32_character_encryption_key
   ```

5. **Deploy**
   - Click "Create Web Service"
   - Wait for build to complete (2-3 minutes)

### **Step 3: Get Your URLs**
After deployment, you'll get:
- **Main App**: `https://whatsapp-lead-assistant.onrender.com`
- **Webhook URL**: `https://whatsapp-lead-assistant.onrender.com/webhook`
- **Health Check**: `https://whatsapp-lead-assistant.onrender.com/health`

## 📱 **Configure Twilio WhatsApp Business**

### **Step 1: Set Webhook URL**
1. Go to [Twilio Console](https://console.twilio.com)
2. Navigate to Messaging → Settings → WhatsApp Sandbox
3. Set Webhook URL to: `https://whatsapp-lead-assistant.onrender.com/webhook`
4. Set HTTP Method to: `POST`

### **Step 2: Test Your Webhook**
```bash
# Test the webhook endpoint
curl -X POST https://whatsapp-lead-assistant.onrender.com/webhook \
  -d "From=whatsapp:+1234567890&Body=Hello&MessageSid=test123" \
  -H "Content-Type: application/x-www-form-urlencoded"
```

Expected response:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>Hello! 👋 I'm your lead assistant. I can help you schedule a consultation call. Would you like to provide your information so I can set up a meeting for you?</Message>
</Response>
```

## 🧪 **Test Your Deployment**

### **Test 1: Health Check**
Visit: `https://whatsapp-lead-assistant.onrender.com/health`

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00",
  "environment_variables": {
    "TWILIO_ACCOUNT_SID": "set",
    "TWILIO_AUTH_TOKEN": "set",
    ...
  },
  "missing_variables": 0,
  "python_version": "3.8.0",
  "rasa_enabled": false
}
```

### **Test 2: Main App**
Visit: `https://whatsapp-lead-assistant.onrender.com`

Should show the app status page.

### **Test 3: WhatsApp Integration**
1. Send a WhatsApp message to your Twilio number
2. You should receive an automated response
3. Check the logs in Render dashboard

## 💰 **Set Up Billing Dashboard**

### **Deploy Billing Dashboard (Optional)**
```bash
# Run locally for now
python billing/billing_dashboard.py
# Visit: http://localhost:8001
```

### **Add Your First Customer**
1. Go to billing dashboard
2. Click "Add New Customer"
3. Fill in customer details
4. Generate invoice
5. Send payment instructions

## 🔧 **Troubleshooting**

### **Common Issues**

**1. Build Fails**
- Check Python version compatibility
- Verify all dependencies in requirements.txt
- Check build logs in Render dashboard

**2. App Won't Start**
- Verify start command: `python main_simple.py`
- Check environment variables are set
- Review logs in Render dashboard

**3. Webhook Not Working**
- Verify webhook URL is correct
- Check Twilio configuration
- Test webhook endpoint manually

**4. Environment Variables Missing**
- Add all required variables in Render dashboard
- Check variable names match exactly
- Restart service after adding variables

### **Debug Commands**
```bash
# Check app logs
# Go to Render dashboard → Logs

# Test webhook locally
curl -X POST http://localhost:8000/webhook \
  -d "From=whatsapp:+1234567890&Body=Test&MessageSid=test123" \
  -H "Content-Type: application/x-www-form-urlencoded"

# Check health endpoint
curl https://whatsapp-lead-assistant.onrender.com/health
```

## 📊 **Monitor Your App**

### **Render Dashboard**
- **Logs**: Real-time application logs
- **Metrics**: CPU, memory usage
- **Deployments**: Build history
- **Environment**: Variable management

### **Health Monitoring**
- **UptimeRobot**: Free uptime monitoring
- **Render Alerts**: Built-in monitoring
- **Custom Health Checks**: `/health` endpoint

## 🚀 **Scale Your Deployment**

### **Free to Pro Upgrade**
When you have customers:
1. Go to Render dashboard
2. Click "Upgrade" on your service
3. Select "Pro" plan ($7/month)
4. Get custom domain, SSL, better performance

### **Custom Domain**
1. Buy domain (Namecheap, GoDaddy, etc.)
2. Add custom domain in Render
3. Configure DNS records
4. Enable SSL certificate

### **Performance Optimization**
- Enable caching
- Optimize database queries
- Use CDN for static files
- Monitor resource usage

## 📈 **Post-Deployment Checklist**

- [ ] ✅ App deployed successfully
- [ ] ✅ Health check passing
- [ ] ✅ Webhook responding correctly
- [ ] ✅ Twilio configured
- [ ] ✅ Environment variables set
- [ ] ✅ Test WhatsApp message received
- [ ] ✅ Billing system ready
- [ ] ✅ First customer added
- [ ] ✅ Invoice generated
- [ ] ✅ Payment received

## 🎉 **You're Ready to Accept Customers!**

Your WhatsApp Lead Assistant is now live and ready to:
- ✅ Receive WhatsApp messages
- ✅ Process lead information
- ✅ Send automated responses
- ✅ Generate invoices
- ✅ Track payments
- ✅ Scale with your business

**Next Steps:**
1. **Market your service** to potential customers
2. **Add customers** to your billing system
3. **Monitor performance** and usage
4. **Gather feedback** and improve
5. **Scale up** when ready

**Your SaaS business is now live! 🚀** 