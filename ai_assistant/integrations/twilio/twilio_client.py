import os
import logging
import requests
from typing import Dict, Any, Optional
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

logger = logging.getLogger(__name__)

class TwilioClient:
    """Client for interacting with Twilio WhatsApp API"""
    
    def __init__(self):
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.phone_number = os.getenv('TWILIO_PHONE_NUMBER')
        
        if not all([self.account_sid, self.auth_token, self.phone_number]):
            logger.error("Twilio credentials not found in environment variables")
            raise ValueError("Twilio credentials are required")
        
        self.client = Client(self.account_sid, self.auth_token)
    
    def send_whatsapp_message(self, to_number: str, message: str) -> Dict[str, Any]:
        """Send WhatsApp message via Twilio"""
        try:
            # Ensure number is in WhatsApp format
            if not to_number.startswith('whatsapp:'):
                to_number = f"whatsapp:{to_number}"
            
            message = self.client.messages.create(
                from_=self.phone_number,
                body=message,
                to=to_number
            )
            
            return {
                "success": True,
                "message_sid": message.sid,
                "status": message.status
            }
            
        except Exception as e:
            logger.error(f"Error sending WhatsApp message: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def send_reminder_message(self, phone: str, name: str, reminder_type: str) -> Dict[str, Any]:
        """Send reminder message for scheduled meeting"""
        try:
            if reminder_type == "5_hour":
                message = f"Hi {name}! 👋 This is a friendly reminder that you have a consultation call scheduled in 5 hours. Please make sure you're available and have any questions ready. We're looking forward to speaking with you!"
            elif reminder_type == "1_hour":
                message = f"Hi {name}! ⏰ Your consultation call is scheduled in 1 hour. Please be ready for the call. If you need to reschedule, please let us know as soon as possible."
            else:
                message = f"Hi {name}! This is a reminder about your upcoming consultation call."
            
            return self.send_whatsapp_message(phone, message)
            
        except Exception as e:
            logger.error(f"Error sending reminder message: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def send_calendly_link(self, phone: str, name: str, booking_link: str) -> Dict[str, Any]:
        """Send Calendly booking link to user"""
        try:
            message = f"Hi {name}! 🎉 Here's your personalized booking link for your consultation:\n\n{booking_link}\n\nPlease click the link to schedule your call. I'll send you reminders before the meeting. If you have any questions, feel free to ask!"
            
            return self.send_whatsapp_message(phone, message)
            
        except Exception as e:
            logger.error(f"Error sending Calendly link: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def send_error_message(self, phone: str, error_type: str = "general") -> Dict[str, Any]:
        """Send error message to user"""
        try:
            if error_type == "processing":
                message = "I'm sorry, but I encountered an issue processing your information. Please try again or contact our support team for assistance."
            elif error_type == "booking":
                message = "I'm sorry, but I couldn't generate a booking link at the moment. Please contact our support team for assistance."
            else:
                message = "I'm sorry, but something went wrong. Please try again or contact our support team."
            
            return self.send_whatsapp_message(phone, message)
            
        except Exception as e:
            logger.error(f"Error sending error message: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def create_webhook_response(self, message: str) -> str:
        """Create TwiML response for webhook"""
        try:
            resp = MessagingResponse()
            resp.message(message)
            return str(resp)
            
        except Exception as e:
            logger.error(f"Error creating webhook response: {str(e)}")
            # Fallback response
            resp = MessagingResponse()
            resp.message("Thank you for your message. We'll get back to you soon.")
            return str(resp)
    
    def validate_webhook_request(self, request_data: Dict[str, Any]) -> bool:
        """Validate incoming webhook request from Twilio"""
        try:
            # Basic validation - in production, add signature validation
            required_fields = ['From', 'Body', 'MessageSid']
            
            for field in required_fields:
                if field not in request_data:
                    logger.warning(f"Missing required field in webhook: {field}")
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error validating webhook request: {str(e)}")
            return False
    
    def get_message_status(self, message_sid: str) -> Optional[Dict[str, Any]]:
        """Get status of a sent message"""
        try:
            message = self.client.messages(message_sid).fetch()
            
            return {
                "sid": message.sid,
                "status": message.status,
                "direction": message.direction,
                "date_created": message.date_created,
                "date_sent": message.date_sent,
                "error_code": message.error_code,
                "error_message": message.error_message
            }
            
        except Exception as e:
            logger.error(f"Error getting message status: {str(e)}")
            return None
    
    def get_account_info(self) -> Optional[Dict[str, Any]]:
        """Get Twilio account information"""
        try:
            account = self.client.api.accounts(self.account_sid).fetch()
            
            return {
                "sid": account.sid,
                "name": account.friendly_name,
                "status": account.status,
                "type": account.type,
                "date_created": account.date_created
            }
            
        except Exception as e:
            logger.error(f"Error getting account info: {str(e)}")
            return None 