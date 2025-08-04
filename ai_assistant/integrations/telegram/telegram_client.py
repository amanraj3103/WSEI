"""
Telegram Bot Client for WhatsApp Lead Assistant Testing
Easy way to test bot functionalities using Telegram
"""

import os
import logging
import asyncio
from typing import Dict, Any, Optional
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class TelegramBotClient:
    """Telegram bot client for testing WhatsApp Lead Assistant"""
    
    def __init__(self, token: str = None):
        self.token = token or os.getenv('TELEGRAM_BOT_TOKEN')
        if not self.token:
            raise ValueError("Telegram bot token is required. Set TELEGRAM_BOT_TOKEN in .env file")
        
        self.bot = Bot(token=self.token)
        self.application = Application.builder().token(self.token).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        """Setup bot command and message handlers"""
        
        # Command handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("schedule", self.schedule_command))
        self.application.add_handler(CommandHandler("status", self.status_command))
        
        # Message handler for all text messages
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        welcome_message = """
🤖 **Welcome to WhatsApp Lead Assistant (Telegram Test)**

I'm here to help you test the lead assistant functionalities!

**Available Commands:**
/start - Show this welcome message
/help - Show help information
/schedule - Start scheduling process
/status - Check bot status

**Features:**
✅ Lead information collection
✅ Meeting scheduling
✅ Automated responses
✅ Integration testing

Send me any message to test the conversation flow!
        """
        
        await update.message.reply_text(welcome_message, parse_mode='Markdown')
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_message = """
📋 **Help - WhatsApp Lead Assistant**

**How to test:**
1. Send me a greeting (hello, hi, etc.)
2. I'll ask for your information
3. Provide your details step by step
4. I'll help you schedule a meeting

**Test Scenarios:**
- Basic conversation flow
- Lead information collection
- Meeting scheduling
- Error handling

**Commands:**
/start - Welcome message
/help - This help message
/schedule - Start scheduling
/status - Bot status

**Example conversation:**
You: "Hello"
Bot: "Hello! I can help you schedule a consultation..."
You: "Yes, I'm interested"
Bot: "Great! What's your name?"
        """
        
        await update.message.reply_text(help_message, parse_mode='Markdown')
    
    async def schedule_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /schedule command"""
        schedule_message = """
📅 **Meeting Scheduling**

Let me help you schedule a consultation call!

**What I need from you:**
1. Your full name
2. Email address
3. Phone number
4. Company name
5. Preferred date/time
6. Service type

**Available time slots:**
- Monday-Friday: 9 AM - 6 PM
- Saturday: 10 AM - 2 PM
- Sunday: Closed

Just send me your name to get started!
        """
        
        await update.message.reply_text(schedule_message, parse_mode='Markdown')
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /status command"""
        status_message = """
📊 **Bot Status**

**Status:** ✅ Online and Ready
**Version:** 1.0.0 (Telegram Test)
**Features:** All systems operational

**Environment Variables:**
- Telegram Bot: ✅ Connected
- Twilio: ⚠️ Not configured (testing mode)
- HubSpot: ⚠️ Not configured (testing mode)
- Calendly: ⚠️ Not configured (testing mode)

**Test Mode:** Active
**Real Integrations:** Disabled for testing
        """
        
        await update.message.reply_text(status_message, parse_mode='Markdown')
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle incoming text messages"""
        user_message = update.message.text.lower()
        user_id = update.effective_user.id
        username = update.effective_user.username or "Unknown"
        
        logger.info(f"Message from {username} ({user_id}): {user_message}")
        
        # Process message using the same logic as WhatsApp
        response = self.process_message(user_message, user_id, username)
        
        await update.message.reply_text(response, parse_mode='Markdown')
    
    def process_message(self, message: str, user_id: int, username: str) -> str:
        """Process message using the same logic as WhatsApp webhook"""
        
        # Simple message processing (same as main_simple.py)
        if any(word in message for word in ['hello', 'hi', 'hey', 'start']):
            return """👋 **Hello! I'm your lead assistant.**

I can help you schedule a consultation call and collect your information.

**Would you like to:**
1. Schedule a meeting
2. Learn more about our services
3. Get pricing information

Just let me know what you'd like to do!"""
        
        elif any(word in message for word in ['schedule', 'consultation', 'meeting', 'call', 'appointment']):
            return """📅 **Great! Let's schedule your consultation.**

I'll need some information from you to set up the meeting.

**Please provide your full name first:**
(Example: John Smith)"""
        
        elif any(word in message for word in ['name', 'i am', 'my name is', 'call me']):
            # Extract name from message
            name = self.extract_name(message)
            return f"""✅ **Thanks {name}!**

**Next, please provide your email address:**
(Example: john@example.com)"""
        
        elif '@' in message and '.' in message:
            # Likely an email
            return """✅ **Email received!**

**Now, please provide your phone number:**
(Example: +1234567890)"""
        
        elif any(char.isdigit() for char in message) and len(message) >= 10:
            # Likely a phone number
            return """✅ **Phone number received!**

**What's your company name?**
(Example: ABC Company)"""
        
        elif any(word in message for word in ['company', 'business', 'organization', 'firm']):
            return """✅ **Company information received!**

**What type of service are you interested in?**
- Study consultation
- Business consultation
- Technical support
- Other

Please let me know your preference."""
        
        elif any(word in message for word in ['study', 'education', 'learning', 'course']):
            return """📚 **Study consultation selected!**

**When would you prefer to have the meeting?**
- Tomorrow
- This week
- Next week
- Specific date

Please let me know your preference."""
        
        elif any(word in message for word in ['tomorrow', 'today', 'this week', 'next week']):
            return """📅 **Perfect!**

**What time works best for you?**
- Morning (9 AM - 12 PM)
- Afternoon (12 PM - 3 PM)
- Evening (3 PM - 6 PM)

Please let me know your preference."""
        
        elif any(word in message for word in ['morning', 'afternoon', 'evening', 'am', 'pm']):
            return """⏰ **Time slot selected!**

**Thank you for providing your information!**

📋 **Summary:**
- Service: Study consultation
- Preferred time: [Time slot]

I'll send you a meeting link shortly. 

**Is there anything else you'd like to know?**"""
        
        elif any(word in message for word in ['bye', 'goodbye', 'stop', 'end']):
            return """👋 **Thank you for your time!**

Have a great day! Feel free to message me again if you need help.

**Bot Status:** Ready for next conversation"""
        
        elif 'help' in message:
            return """❓ **How can I help you?**

**Available options:**
1. Schedule a consultation
2. Get pricing information
3. Learn about services
4. Contact support

**Commands:**
/start - Welcome message
/help - This help message
/schedule - Start scheduling
/status - Bot status

Just let me know what you'd like to do!"""
        
        else:
            return """🤔 **I didn't quite understand that.**

**You can:**
- Say "hello" to start
- Type "schedule" to book a consultation
- Type "help" for assistance
- Use /help for commands

**Or just tell me what you're looking for!**"""
    
    def extract_name(self, message: str) -> str:
        """Extract name from message"""
        # Simple name extraction
        words = message.split()
        for i, word in enumerate(words):
            if word.lower() in ['name', 'is', 'am', 'call']:
                if i + 1 < len(words):
                    return words[i + 1].title()
        
        # If no clear name found, return first word
        return words[0].title() if words else "there"
    
    async def start_polling(self):
        """Start the bot polling"""
        logger.info("Starting Telegram bot...")
        await self.application.initialize()
        await self.application.start()
        await self.application.updater.start_polling()
        
        logger.info("Telegram bot started successfully!")
        logger.info("Bot is now listening for messages...")
        
        try:
            # Keep the bot running
            await asyncio.Event().wait()
        except KeyboardInterrupt:
            logger.info("Stopping Telegram bot...")
            await self.application.updater.stop()
            await self.application.stop()
            await self.application.shutdown()
    
    def run(self):
        """Run the bot (synchronous wrapper)"""
        asyncio.run(self.start_polling())

# Example usage
if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    try:
        # Create and run bot
        bot = TelegramBotClient()
        bot.run()
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
        print(f"❌ Error: {e}")
        print("Make sure TELEGRAM_BOT_TOKEN is set in your .env file") 