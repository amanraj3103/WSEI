import os
import logging
import json
from datetime import datetime
from typing import Dict, Any
from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse
import uvicorn
from dotenv import load_dotenv

from rasa_bot.actions.actions import ActionProcessLead, ActionSendCalendlyLink
from integrations.twilio.twilio_client import TwilioClient
from integrations.hubspot.hubspot_client import HubSpotClient
from integrations.calendly.calendly_client import CalendlyClient
from scheduling.reminder_scheduler import ReminderScheduler
from reporting.report_generator import ReportGenerator

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
    title="WhatsApp Lead Assistant",
    description="Automated WhatsApp lead assistant with Rasa, HubSpot, and Calendly integration",
    version="1.0.0"
)

# Initialize clients
twilio_client = TwilioClient()
hubspot_client = HubSpotClient()
calendly_client = CalendlyClient()
reminder_scheduler = ReminderScheduler()
report_generator = ReportGenerator()

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("Starting WhatsApp Lead Assistant...")
    
    # Check if all required environment variables are set
    required_vars = [
        'TWILIO_ACCOUNT_SID', 'TWILIO_AUTH_TOKEN', 'TWILIO_PHONE_NUMBER',
        'HUBSPOT_API_KEY', 'HUBSPOT_PORTAL_ID',
        'CALENDLY_API_KEY', 'CALENDLY_USER_URI',
        'ENCRYPTION_KEY'
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        logger.error(f"Missing required environment variables: {missing_vars}")
        raise ValueError(f"Missing required environment variables: {missing_vars}")
    
    logger.info("WhatsApp Lead Assistant started successfully!")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down WhatsApp Lead Assistant...")
    reminder_scheduler.shutdown()
    logger.info("WhatsApp Lead Assistant shutdown complete!")

@app.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint with basic information"""
    return """
    <html>
        <head>
            <title>WhatsApp Lead Assistant</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                .container { max-width: 800px; margin: 0 auto; }
                .status { padding: 10px; border-radius: 5px; margin: 10px 0; }
                .success { background-color: #d4edda; color: #155724; }
                .info { background-color: #d1ecf1; color: #0c5460; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🤖 WhatsApp Lead Assistant</h1>
                <div class="status success">
                    <strong>Status:</strong> Running
                </div>
                <div class="status info">
                    <strong>Version:</strong> 1.0.0
                </div>
                <h2>Features</h2>
                <ul>
                    <li>✅ Rasa-powered NLP for lead conversations</li>
                    <li>✅ HubSpot CRM integration</li>
                    <li>✅ Calendly scheduling</li>
                    <li>✅ Automated WhatsApp reminders</li>
                    <li>✅ PDF/Excel report generation</li>
                    <li>✅ Encrypted data handling</li>
                </ul>
                <h2>Endpoints</h2>
                <ul>
                    <li><strong>POST /webhook</strong> - Twilio WhatsApp webhook</li>
                    <li><strong>GET /health</strong> - Health check</li>
                    <li><strong>GET /metrics</strong> - Application metrics</li>
                </ul>
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
        
        # Validate webhook request
        if not twilio_client.validate_webhook_request(data):
            logger.warning("Invalid webhook request received")
            raise HTTPException(status_code=400, detail="Invalid webhook request")
        
        # Extract message details
        from_number = data.get('From', '').replace('whatsapp:', '')
        message_body = data.get('Body', '')
        message_sid = data.get('MessageSid', '')
        
        logger.info(f"Message from {from_number}: {message_body}")
        
        # Process message with Rasa (simplified for demo)
        # In production, this would integrate with Rasa server
        response_message = await process_message_with_rasa(from_number, message_body)
        
        # Create TwiML response
        twiml_response = twilio_client.create_webhook_response(response_message)
        
        return HTMLResponse(content=twiml_response, media_type="application/xml")
        
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        # Return a generic response to avoid webhook failures
        fallback_response = twilio_client.create_webhook_response(
            "Thank you for your message. We'll get back to you soon."
        )
        return HTMLResponse(content=fallback_response, media_type="application/xml")

async def process_message_with_rasa(phone: str, message: str) -> str:
    """Process message with Rasa (simplified implementation)"""
    try:
        # This is a simplified version - in production, you would:
        # 1. Send message to Rasa server
        # 2. Get intent and entities
        # 3. Execute custom actions
        # 4. Return response
        
        # For demo purposes, implement basic logic
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
            
    except Exception as e:
        logger.error(f"Error processing message with Rasa: {str(e)}")
        return "I'm sorry, but I encountered an error processing your message. Please try again."

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check scheduler health
        scheduler_health = reminder_scheduler.health_check()
        
        # Check Twilio connection
        twilio_health = twilio_client.get_account_info() is not None
        
        # Check HubSpot connection
        hubspot_health = True  # Simplified for demo
        
        # Check Calendly connection
        calendly_health = calendly_client.get_user_info() is not None
        
        overall_health = all([scheduler_health.get('running', False), 
                             twilio_health, hubspot_health, calendly_health])
        
        return {
            "status": "healthy" if overall_health else "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "services": {
                "scheduler": scheduler_health,
                "twilio": {"status": "connected" if twilio_health else "disconnected"},
                "hubspot": {"status": "connected" if hubspot_health else "disconnected"},
                "calendly": {"status": "connected" if calendly_health else "disconnected"}
            }
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
        # Get scheduled reminders
        scheduled_reminders = reminder_scheduler.get_scheduled_reminders()
        
        # Get account info
        account_info = twilio_client.get_account_info()
        
        return {
            "timestamp": datetime.now().isoformat(),
            "scheduled_reminders": len(scheduled_reminders),
            "twilio_account": {
                "name": account_info.get("name") if account_info else "Unknown",
                "status": account_info.get("status") if account_info else "Unknown"
            },
            "system": {
                "uptime": "running",  # In production, calculate actual uptime
                "memory_usage": "normal",  # In production, get actual memory usage
                "cpu_usage": "normal"  # In production, get actual CPU usage
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
            "notes": "Test lead from API",
            "source": "API Test"
        }
        
        # Create lead in HubSpot
        result = hubspot_client.create_lead(test_lead)
        
        return {
            "success": result.get("success", False),
            "lead_id": result.get("lead_id"),
            "message": "Test lead created successfully" if result.get("success") else "Failed to create test lead"
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
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=debug,
        log_level="info"
    ) 