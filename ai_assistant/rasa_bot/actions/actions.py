import sys
import os
import json
import logging
from typing import Any, Text, Dict, List
from datetime import datetime, timedelta

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from integrations.hubspot.hubspot_client import HubSpotClient
from integrations.calendly.calendly_client import CalendlyClient
from integrations.twilio.twilio_client import TwilioClient
from integrations.encryption.encryption_utils import EncryptionUtils
from scheduling.reminder_scheduler import ReminderScheduler

logger = logging.getLogger(__name__)

class ActionProcessLead(Action):
    """Process collected lead information and send to HubSpot"""
    
    def name(self) -> Text:
        return "action_process_lead"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            # Get lead information from slots
            name = tracker.get_slot("name")
            email = tracker.get_slot("email")
            phone = tracker.get_slot("phone")
            country = tracker.get_slot("country")
            service_type = tracker.get_slot("service_type")
            preferred_date = tracker.get_slot("preferred_date")
            preferred_time = tracker.get_slot("preferred_time")
            notes = tracker.get_slot("notes")
            
            # Validate required fields
            if not all([name, email, phone, country, service_type]):
                dispatcher.utter_message(text="I'm sorry, but I need all the required information to process your lead. Please provide the missing details.")
                return []
            
            # Encrypt sensitive data
            encryption_utils = EncryptionUtils()
            encrypted_email = encryption_utils.encrypt(email)
            encrypted_phone = encryption_utils.encrypt(phone)
            
            # Prepare lead data
            lead_data = {
                "name": name,
                "email": encrypted_email,
                "phone": encrypted_phone,
                "country": country,
                "service_type": service_type,
                "preferred_date": preferred_date,
                "preferred_time": preferred_time,
                "notes": notes or "",
                "source": "WhatsApp",
                "created_at": datetime.now().isoformat()
            }
            
            # Send to HubSpot
            hubspot_client = HubSpotClient()
            hubspot_response = hubspot_client.create_lead(lead_data)
            
            if hubspot_response.get("success"):
                # Store lead ID for scheduling reminders
                lead_id = hubspot_response.get("lead_id")
                tracker.slots["lead_id"] = lead_id
                
                # Schedule reminders if date/time provided
                if preferred_date and preferred_time:
                    self._schedule_reminders(lead_id, name, phone, preferred_date, preferred_time)
                
                dispatcher.utter_message(text="Great! I've successfully processed your information and created your lead in our system.")
                return [SlotSet("lead_id", lead_id)]
            else:
                dispatcher.utter_message(text="I encountered an issue processing your information. Please try again or contact our support team.")
                return []
                
        except Exception as e:
            logger.error(f"Error processing lead: {str(e)}")
            dispatcher.utter_message(text="I'm sorry, but I encountered an error processing your information. Please try again.")
            return []
    
    def _schedule_reminders(self, lead_id: str, name: str, phone: str, date: str, time: str):
        """Schedule WhatsApp reminders for the meeting"""
        try:
            scheduler = ReminderScheduler()
            
            # Parse date and time (simplified - in production, use proper date parsing)
            meeting_datetime = datetime.now() + timedelta(days=1)  # Default to tomorrow
            
            # Schedule 5-hour reminder
            five_hour_reminder = meeting_datetime - timedelta(hours=5)
            scheduler.schedule_reminder(
                lead_id=lead_id,
                phone=phone,
                name=name,
                reminder_time=five_hour_reminder,
                reminder_type="5_hour"
            )
            
            # Schedule 1-hour reminder
            one_hour_reminder = meeting_datetime - timedelta(hours=1)
            scheduler.schedule_reminder(
                lead_id=lead_id,
                phone=phone,
                name=name,
                reminder_time=one_hour_reminder,
                reminder_type="1_hour"
            )
            
        except Exception as e:
            logger.error(f"Error scheduling reminders: {str(e)}")

class ActionSendCalendlyLink(Action):
    """Send personalized Calendly booking link to user"""
    
    def name(self) -> Text:
        return "action_send_calendly_link"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            # Get user information
            name = tracker.get_slot("name")
            service_type = tracker.get_slot("service_type")
            country = tracker.get_slot("country")
            
            # Create personalized Calendly link
            calendly_client = CalendlyClient()
            booking_link = calendly_client.create_booking_link(
                name=name,
                service_type=service_type,
                country=country
            )
            
            if booking_link:
                message = f"Perfect! Here's your personalized booking link for your consultation:\n\n{booking_link}\n\nPlease click the link to schedule your call. I'll send you reminders before the meeting. If you have any questions, feel free to ask!"
                dispatcher.utter_message(text=message)
            else:
                dispatcher.utter_message(text="I'm sorry, but I couldn't generate a booking link at the moment. Please contact our support team for assistance.")
                
        except Exception as e:
            logger.error(f"Error sending Calendly link: {str(e)}")
            dispatcher.utter_message(text="I encountered an issue generating your booking link. Please try again or contact our support team.")
        
        return []

class ActionGenerateReport(Action):
    """Generate PDF/Excel report for the lead conversation"""
    
    def name(self) -> Text:
        return "action_generate_report"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            from reporting.report_generator import ReportGenerator
            
            lead_id = tracker.get_slot("lead_id")
            if not lead_id:
                return []
            
            # Generate report
            report_generator = ReportGenerator()
            report_path = report_generator.generate_lead_report(lead_id)
            
            if report_path:
                # Send report to admin (in production, this would be via email)
                logger.info(f"Lead report generated: {report_path}")
                
        except Exception as e:
            logger.error(f"Error generating report: {str(e)}")
        
        return []

class ActionValidateEmail(Action):
    """Validate email format"""
    
    def name(self) -> Text:
        return "action_validate_email"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        email = tracker.get_slot("email")
        if email and "@" not in email:
            dispatcher.utter_message(text="Please provide a valid email address.")
            return [SlotSet("email", None)]
        
        return []

class ActionValidatePhone(Action):
    """Validate phone number format"""
    
    def name(self) -> Text:
        return "action_validate_phone"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        phone = tracker.get_slot("phone")
        if phone and len(phone.replace("+", "").replace(" ", "").replace("-", "")) < 10:
            dispatcher.utter_message(text="Please provide a valid phone number with country code (e.g., +1234567890).")
            return [SlotSet("phone", None)]
        
        return [] 