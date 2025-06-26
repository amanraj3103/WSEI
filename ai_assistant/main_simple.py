import os
import logging
import json
from datetime import datetime
from typing import Dict, Any
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
import uvicorn
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="WhatsApp Lead Assistant (Simple)",
    description="Simplified WhatsApp lead assistant for testing",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("Starting WhatsApp Lead Assistant (Simple)...")
    
    # Check if all required environment variables are set
    required_vars = [
        'TWILIO_ACCOUNT_SID', 'TWILIO_AUTH_TOKEN', 'TWILIO_PHONE_NUMBER',
        'HUBSPOT_API_KEY', 'HUBSPOT_PORTAL_ID',
        'CALENDLY_API_KEY', 'CALENDLY_USER_URI',
        'ENCRYPTION_KEY'
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        logger.warning(f"Missing environment variables: {missing_vars}")
        logger.warning("Some features may not work properly")
    else:
        logger.info("All required environment variables are set!")
    
    logger.info("WhatsApp Lead Assistant (Simple) started successfully!")

@app.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint with basic information"""
    return """
    <html>
        <head>
            <title>WhatsApp Lead Assistant (Simple)</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                .container { max-width: 800px; margin: 0 auto; }
                .status { padding: 10px; border-radius: 5px; margin: 10px 0; }
                .success { background-color: #d4edda; color: #155724; }
                .warning { background-color: #fff3cd; color: #856404; }
                .info { background-color: #d1ecf1; color: #0c5460; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🤖 WhatsApp Lead Assistant (Simple)</h1>
                <div class="status success">
                    <strong>Status:</strong> Running (Simplified Version)
                </div>
                <div class="status info">
                    <strong>Version:</strong> 1.0.0 (Python 3.8 Compatible)
                </div>
                <div class="status warning">
                    <strong>Note:</strong> This is a simplified version without Rasa NLP
                </div>
                <h2>Features</h2>
                <ul>
                    <li>✅ FastAPI web server</li>
                    <li>✅ Environment variable validation</li>
                    <li>✅ Health check endpoints</li>
                    <li>✅ Basic webhook structure</li>
                    <li>⚠️ Rasa NLP (disabled for Python 3.8 compatibility)</li>
                    <li>⚠️ HubSpot integration (requires setup)</li>
                    <li>⚠️ Calendly integration (requires setup)</li>
                </ul>
                <h2>Endpoints</h2>
                <ul>
                    <li><strong>POST /webhook</strong> - Twilio WhatsApp webhook</li>
                    <li><strong>GET /health</strong> - Health check</li>
                    <li><strong>GET /metrics</strong> - Application metrics</li>
                    <li><strong>POST /test-lead</strong> - Test lead creation</li>
                </ul>
                <h2>Next Steps</h2>
                <ol>
                    <li>Configure your .env file with API keys</li>
                    <li>Test the basic endpoints</li>
                    <li>Upgrade to Python 3.9+ for full Rasa functionality</li>
                    <li>Deploy to production</li>
                </ol>
            </div>
        </body>
    </html>
    """

@app.post("/webhook")
async def twilio_webhook(request: Request):
    """Handle incoming WhatsApp messages from Twilio"""
    try:
        # Parse form data from Twilio
        form_data = await request.form()
        data = dict(form_data)
        
        logger.info(f"Received webhook: {data}")
        
        # Extract message details
        from_number = data.get('From', '').replace('whatsapp:', '')
        message_body = data.get('Body', '')
        message_sid = data.get('MessageSid', '')
        
        logger.info(f"Message from {from_number}: {message_body}")
        
        # Simple response logic (without Rasa)
        response_message = process_simple_message(message_body)
        
        # Create simple TwiML response
        twiml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{response_message}</Message>
</Response>"""
        
        return HTMLResponse(content=twiml_response, media_type="application/xml")
        
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        # Return a generic response to avoid webhook failures
        fallback_response = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>Thank you for your message. We'll get back to you soon.</Message>
</Response>"""
        return HTMLResponse(content=fallback_response, media_type="application/xml")

def process_simple_message(message: str) -> str:
    """Simple message processing without Rasa"""
    message_lower = message.lower()
    
    if any(word in message_lower for word in ['hello', 'hi', 'hey']):
        return "Hello! 👋 I'm your lead assistant. I can help you schedule a consultation call. Would you like to provide your information so I can set up a meeting for you?"
    
    elif any(word in message_lower for word in ['schedule', 'consultation', 'meeting', 'call']):
        return "Great! I'll help you schedule a consultation. Let me collect some information from you. What's your full name?"
    
    elif any(word in message_lower for word in ['bye', 'goodbye', 'stop']):
        return "Thank you for your time! Have a great day! 👋"
    
    elif 'help' in message_lower:
        return "I'm here to help you schedule a consultation call. I'll ask you a few questions to collect your information and then send you a booking link. You can say 'stop' at any time to end the conversation."
    
    else:
        return "I'm sorry, I didn't understand that. I can help you schedule a consultation call. Would you like to start?"

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check environment variables
        env_status = {}
        required_vars = [
            'TWILIO_ACCOUNT_SID', 'TWILIO_AUTH_TOKEN', 'TWILIO_PHONE_NUMBER',
            'HUBSPOT_API_KEY', 'HUBSPOT_PORTAL_ID',
            'CALENDLY_API_KEY', 'CALENDLY_USER_URI',
            'ENCRYPTION_KEY'
        ]
        
        for var in required_vars:
            env_status[var] = "set" if os.getenv(var) else "missing"
        
        missing_count = sum(1 for status in env_status.values() if status == "missing")
        overall_health = missing_count == 0
        
        return {
            "status": "healthy" if overall_health else "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "environment_variables": env_status,
            "missing_variables": missing_count,
            "python_version": "3.8.0",
            "rasa_enabled": False
        }
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }

@app.get("/metrics")
async def get_metrics():
    """Get application metrics"""
    try:
        return {
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0 (Simple)",
            "python_version": "3.8.0",
            "rasa_enabled": False,
            "features": {
                "webhook_processing": True,
                "health_monitoring": True,
                "metrics_collection": True,
                "rasa_nlp": False,
                "hubspot_integration": False,
                "calendly_integration": False
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting metrics: {str(e)}")
        return {
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }

@app.post("/test-lead")
async def test_lead_creation():
    """Test endpoint for lead creation (for development)"""
    try:
        # Create test lead data
        test_lead = {
            "name": "Test User",
            "email": "test@example.com",
            "phone": "+1234567890",
            "country": "United States",
            "service_type": "study",
            "preferred_date": "tomorrow",
            "preferred_time": "2 PM",
            "notes": "Test lead from API (Simple Version)",
            "source": "API Test"
        }
        
        logger.info(f"Test lead created: {test_lead}")
        
        return {
            "success": True,
            "message": "Test lead created successfully (Simple Version)",
            "lead_data": test_lead,
            "note": "HubSpot integration not available in simple version"
        }
        
    except Exception as e:
        logger.error(f"Error creating test lead: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    # Run the application
    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("DEBUG", "False").lower() == "true"
    
    uvicorn.run(
        "main_simple:app",
        host="0.0.0.0",
        port=port,
        reload=debug,
        log_level="info"
    ) 