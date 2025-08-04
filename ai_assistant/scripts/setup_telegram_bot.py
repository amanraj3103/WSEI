#!/usr/bin/env python3
"""
Setup script for Telegram Bot Testing
Helps you create a Telegram bot and get the token
"""

import os
import sys
import requests
import json
from pathlib import Path

def create_telegram_bot():
    """Guide user through creating a Telegram bot"""
    
    print("🤖 Telegram Bot Setup for WhatsApp Lead Assistant Testing")
    print("=" * 60)
    
    print("\n📱 Step 1: Create a Telegram Bot")
    print("1. Open Telegram app on your phone/computer")
    print("2. Search for '@BotFather'")
    print("3. Send /start to BotFather")
    print("4. Send /newbot to create a new bot")
    print("5. Follow the instructions:")
    print("   - Choose a name for your bot (e.g., 'Lead Assistant Test')")
    print("   - Choose a username (e.g., 'lead_assistant_test_bot')")
    print("6. BotFather will give you a token like: 123456789:ABCdefGHIjklMNOpqrsTUVwxyz")
    
    print("\n🔑 Step 2: Get Your Bot Token")
    token = input("\nEnter your bot token: ").strip()
    
    if not token or ':' not in token:
        print("❌ Invalid token format. Please check your token.")
        return False
    
    print("\n✅ Step 3: Test Your Bot")
    print(f"1. Search for your bot in Telegram: @{token.split(':')[0]}")
    print("2. Send /start to your bot")
    print("3. You should receive a welcome message")
    
    # Save token to .env file
    env_file = Path('.env')
    if env_file.exists():
        # Read existing .env file
        with open(env_file, 'r') as f:
            content = f.read()
        
        # Check if TELEGRAM_BOT_TOKEN already exists
        if 'TELEGRAM_BOT_TOKEN' in content:
            # Replace existing token
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if line.startswith('TELEGRAM_BOT_TOKEN='):
                    lines[i] = f'TELEGRAM_BOT_TOKEN={token}'
                    break
            content = '\n'.join(lines)
        else:
            # Add new token
            content += f'\nTELEGRAM_BOT_TOKEN={token}'
    else:
        # Create new .env file
        content = f'TELEGRAM_BOT_TOKEN={token}'
    
    # Write to .env file
    with open(env_file, 'w') as f:
        f.write(content)
    
    print(f"\n✅ Token saved to .env file")
    
    return True

def test_telegram_bot():
    """Test the Telegram bot connection"""
    
    print("\n🧪 Step 4: Test Bot Connection")
    
    try:
        from integrations.telegram.telegram_client import TelegramBotClient
        
        # Test bot creation
        bot = TelegramBotClient()
        print("✅ Bot client created successfully")
        
        # Test bot info
        bot_info = bot.bot.get_me()
        print(f"✅ Bot connected: @{bot_info.username}")
        print(f"   Name: {bot_info.first_name}")
        print(f"   ID: {bot_info.id}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing bot: {e}")
        return False

def run_telegram_bot():
    """Run the Telegram bot"""
    
    print("\n🚀 Step 5: Start the Bot")
    print("Starting Telegram bot...")
    print("Press Ctrl+C to stop the bot")
    
    try:
        from integrations.telegram.telegram_client import TelegramBotClient
        
        bot = TelegramBotClient()
        bot.run()
        
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
    except Exception as e:
        print(f"❌ Error running bot: {e}")

def main():
    """Main setup function"""
    
    print("🤖 Welcome to Telegram Bot Setup!")
    print("This will help you test your WhatsApp Lead Assistant using Telegram.")
    
    # Check if token already exists
    if os.getenv('TELEGRAM_BOT_TOKEN'):
        print("\n✅ Telegram bot token already found in environment")
        choice = input("Do you want to create a new bot? (y/n): ").lower()
        if choice != 'y':
            print("Using existing token...")
        else:
            if not create_telegram_bot():
                return
    else:
        if not create_telegram_bot():
            return
    
    # Test the bot
    if not test_telegram_bot():
        print("❌ Bot test failed. Please check your token.")
        return
    
    # Ask if user wants to run the bot
    choice = input("\nDo you want to start the bot now? (y/n): ").lower()
    if choice == 'y':
        run_telegram_bot()
    else:
        print("\n📋 To run the bot later:")
        print("python integrations/telegram/telegram_client.py")
        print("or")
        print("python scripts/setup_telegram_bot.py --run")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--run':
        run_telegram_bot()
    else:
        main() 