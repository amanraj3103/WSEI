# 🤖 Telegram Testing Guide - WhatsApp Lead Assistant

## 🎯 **Why Use Telegram for Testing?**

Telegram is perfect for testing your WhatsApp Lead Assistant because:
- ✅ **Free to use** - No API costs
- ✅ **Easy setup** - 5 minutes to get started
- ✅ **Same logic** - Uses identical message processing
- ✅ **Real-time testing** - Instant feedback
- ✅ **No webhook setup** - Simple polling
- ✅ **Cross-platform** - Works on phone, desktop, web

## 🚀 **Quick Setup (5 minutes)**

### **Step 1: Create Telegram Bot**
1. **Open Telegram** on your phone/computer
2. **Search for @BotFather**
3. **Send /start** to BotFather
4. **Send /newbot** to create a new bot
5. **Choose a name**: "Lead Assistant Test"
6. **Choose username**: "lead_assistant_test_bot"
7. **Copy the token** (looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### **Step 2: Set Up the Bot**
```bash
# Run the setup script
python scripts/setup_telegram_bot.py

# Or manually add to .env file
echo "TELEGRAM_BOT_TOKEN=your_token_here" >> .env
```

### **Step 3: Install Dependencies**
```bash
pip install python-telegram-bot==20.3
```

### **Step 4: Start the Bot**
```bash
# Option 1: Use setup script
python scripts/setup_telegram_bot.py --run

# Option 2: Run directly
python integrations/telegram/telegram_client.py
```

## 🧪 **Testing Your Bot**

### **Basic Commands**
- `/start` - Welcome message
- `/help` - Help information
- `/schedule` - Start scheduling process
- `/status` - Bot status

### **Test Conversation Flow**
```
You: /start
Bot: Welcome message with available commands

You: Hello
Bot: "Hello! I'm your lead assistant. I can help you schedule a consultation call..."

You: I want to schedule a meeting
Bot: "Great! Let's schedule your consultation. Please provide your full name first:"

You: My name is John Smith
Bot: "Thanks John! Next, please provide your email address:"

You: john@example.com
Bot: "Email received! Now, please provide your phone number:"

You: +1234567890
Bot: "Phone number received! What's your company name?"

You: ABC Company
Bot: "Company information received! What type of service are you interested in?"

You: Study consultation
Bot: "Study consultation selected! When would you prefer to have the meeting?"

You: Tomorrow
Bot: "Perfect! What time works best for you?"

You: Morning
Bot: "Time slot selected! Thank you for providing your information!"
```

## 📱 **Bot Features**

### **✅ What Works in Telegram**
- **Lead information collection** - Name, email, phone, company
- **Service selection** - Study, business, technical support
- **Meeting scheduling** - Date and time preferences
- **Automated responses** - Context-aware replies
- **Command system** - /start, /help, /schedule, /status
- **Error handling** - Graceful responses to unclear messages

### **⚠️ What's Different from WhatsApp**
- **No Twilio integration** - Uses Telegram API instead
- **No webhook** - Uses polling (simpler for testing)
- **No HubSpot sync** - Data collection only (no CRM integration)
- **No Calendly links** - Simulated scheduling responses
- **No encryption** - Standard Telegram security

## 🔧 **Customization**

### **Modify Bot Responses**
Edit `integrations/telegram/telegram_client.py`:
```python
def process_message(self, message: str, user_id: int, username: str) -> str:
    # Add your custom logic here
    if "custom keyword" in message:
        return "Your custom response"
```

### **Add New Commands**
```python
# In setup_handlers method
self.application.add_handler(CommandHandler("custom", self.custom_command))

# Add the handler method
async def custom_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Your custom command response")
```

### **Store User Data**
```python
# Add to handle_message method
user_data = {
    'user_id': user_id,
    'username': username,
    'last_message': message,
    'conversation_state': 'collecting_name'
}
# Store in database or file
```

## 📊 **Testing Scenarios**

### **Scenario 1: Basic Lead Collection**
1. Start conversation with `/start`
2. Say "I want to schedule a meeting"
3. Provide name, email, phone, company
4. Select service type
5. Choose meeting time
6. Verify all information is collected

### **Scenario 2: Error Handling**
1. Send unclear messages
2. Test with invalid email formats
3. Send empty messages
4. Test with special characters
5. Verify graceful error responses

### **Scenario 3: Edge Cases**
1. Send very long messages
2. Use different languages
3. Send emojis and special characters
4. Test rapid message sending
5. Verify bot stability

## 🚀 **Deploy Telegram Bot**

### **Local Testing**
```bash
# Run locally for development
python integrations/telegram/telegram_client.py
```

### **Server Deployment**
```bash
# Install on server
pip install python-telegram-bot==20.3

# Run with screen or systemd
screen -S telegram_bot
python integrations/telegram/telegram_client.py
```

### **Docker Deployment**
```dockerfile
# Add to Dockerfile
RUN pip install python-telegram-bot==20.3

# Run bot alongside main app
CMD ["python", "integrations/telegram/telegram_client.py"]
```

## 🔍 **Debugging**

### **Common Issues**

**1. Bot Not Responding**
```bash
# Check if bot is running
ps aux | grep telegram

# Check logs
tail -f logs/telegram_bot.log
```

**2. Token Issues**
```bash
# Verify token format
echo $TELEGRAM_BOT_TOKEN

# Test token manually
curl "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getMe"
```

**3. Import Errors**
```bash
# Install dependencies
pip install python-telegram-bot==20.3

# Check Python path
python -c "import telegram; print('OK')"
```

### **Logging**
```python
# Enable detailed logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📈 **Analytics**

### **Track Bot Usage**
```python
# Add to handle_message
def log_user_interaction(user_id, username, message, response):
    # Log to file or database
    with open('telegram_analytics.log', 'a') as f:
        f.write(f"{datetime.now()},{user_id},{username},{message},{response}\n")
```

### **Monitor Performance**
- **Response time** - How fast bot responds
- **User engagement** - Message frequency
- **Completion rate** - How many users complete lead form
- **Error rate** - Failed interactions

## 🎯 **Next Steps**

### **After Telegram Testing**
1. **Validate conversation flow** - Ensure all scenarios work
2. **Optimize responses** - Improve user experience
3. **Add features** - Custom commands, data storage
4. **Deploy to production** - Move to WhatsApp Business API
5. **Scale up** - Handle multiple users

### **Migration to WhatsApp**
1. **Keep Telegram bot** - For testing and development
2. **Deploy WhatsApp version** - Using same logic
3. **Test both platforms** - Ensure consistency
4. **Monitor performance** - Compare user engagement

## 💡 **Pro Tips**

1. **Test thoroughly** - Try all possible user inputs
2. **Document issues** - Keep track of bugs and improvements
3. **Gather feedback** - Ask users about their experience
4. **Iterate quickly** - Make changes based on testing
5. **Backup data** - Save important conversations and data

## 🎉 **You're Ready to Test!**

Your Telegram bot is now ready to test all WhatsApp Lead Assistant functionalities!

**Benefits:**
- ✅ **Free testing** - No API costs
- ✅ **Fast setup** - 5 minutes to start
- ✅ **Real conversations** - Test with real users
- ✅ **Easy debugging** - Simple to modify and test
- ✅ **Production ready** - Same logic as WhatsApp version

**Start testing now and perfect your lead assistant! 🚀** 