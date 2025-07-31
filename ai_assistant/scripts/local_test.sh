#!/bin/bash

echo "🚀 Starting WhatsApp Lead Assistant locally..."

# Create logs directory if it doesn't exist
mkdir -p logs

# Install dependencies if needed
if [ ! -d "venv" ]; then
    echo "📦 Setting up virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Start the application
echo "🌐 Starting FastAPI server..."
python main_simple.py &

# Wait for server to start
sleep 3

# Check if ngrok is installed
if ! command -v ngrok &> /dev/null; then
    echo "❌ ngrok not found. Please install it first:"
    echo "   brew install ngrok/ngrok/ngrok"
    echo "   Then run: ngrok config add-authtoken YOUR_AUTHTOKEN"
    exit 1
fi

# Start ngrok
echo "🔗 Starting ngrok tunnel..."
ngrok http 8000

echo "✅ Setup complete!"
echo "📱 Use the ngrok URL (https://xxxx.ngrok.io) as your Twilio webhook URL" 