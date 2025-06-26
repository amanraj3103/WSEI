import os
import logging
import json
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

from integrations.twilio.twilio_client import TwilioClient
from integrations.encryption.encryption_utils import EncryptionUtils

logger = logging.getLogger(__name__)

class ReminderScheduler:
    """Scheduler for sending WhatsApp reminders before meetings"""
    
    def __init__(self):
        self.scheduler = self._initialize_scheduler()
        self.twilio_client = TwilioClient()
        self.encryption_utils = EncryptionUtils()
        
        # Start the scheduler
        if not self.scheduler.running:
            self.scheduler.start()
    
    def _initialize_scheduler(self) -> BackgroundScheduler:
        """Initialize the APScheduler with SQLAlchemy job store"""
        try:
            # Configure job store
            jobstores = {
                'default': SQLAlchemyJobStore(url='sqlite:///reminders.db')
            }
            
            # Configure scheduler
            scheduler = BackgroundScheduler(
                jobstores=jobstores,
                job_defaults={
                    'coalesce': False,
                    'max_instances': 3
                }
            )
            
            return scheduler
            
        except Exception as e:
            logger.error(f"Error initializing scheduler: {str(e)}")
            # Fallback to memory-based scheduler
            return BackgroundScheduler()
    
    def schedule_reminder(self, lead_id: str, phone: str, name: str, 
                         reminder_time: datetime, reminder_type: str) -> bool:
        """Schedule a WhatsApp reminder"""
        try:
            # Decrypt phone number if needed
            decrypted_phone = self.encryption_utils.decrypt(phone)
            
            # Create job ID
            job_id = f"reminder_{lead_id}_{reminder_type}_{int(reminder_time.timestamp())}"
            
            # Add job to scheduler
            self.scheduler.add_job(
                func=self._send_reminder,
                trigger=DateTrigger(run_date=reminder_time),
                args=[lead_id, decrypted_phone, name, reminder_type],
                id=job_id,
                replace_existing=True
            )
            
            logger.info(f"Scheduled {reminder_type} reminder for lead {lead_id} at {reminder_time}")
            return True
            
        except Exception as e:
            logger.error(f"Error scheduling reminder: {str(e)}")
            return False
    
    def _send_reminder(self, lead_id: str, phone: str, name: str, reminder_type: str):
        """Send the actual reminder message"""
        try:
            logger.info(f"Sending {reminder_type} reminder to {name} ({phone})")
            
            # Send reminder via Twilio
            result = self.twilio_client.send_reminder_message(phone, name, reminder_type)
            
            if result.get("success"):
                logger.info(f"Successfully sent {reminder_type} reminder to {name}")
                
                # Log reminder sent
                self._log_reminder_sent(lead_id, phone, name, reminder_type, result.get("message_sid"))
            else:
                logger.error(f"Failed to send {reminder_type} reminder to {name}: {result.get('error')}")
                
        except Exception as e:
            logger.error(f"Error sending reminder: {str(e)}")
    
    def schedule_5_hour_reminder(self, lead_id: str, phone: str, name: str, 
                                meeting_datetime: datetime) -> bool:
        """Schedule 5-hour reminder before meeting"""
        reminder_time = meeting_datetime - timedelta(hours=5)
        
        # Only schedule if reminder time is in the future
        if reminder_time > datetime.now():
            return self.schedule_reminder(lead_id, phone, name, reminder_time, "5_hour")
        else:
            logger.warning(f"5-hour reminder time {reminder_time} is in the past for lead {lead_id}")
            return False
    
    def schedule_1_hour_reminder(self, lead_id: str, phone: str, name: str, 
                                meeting_datetime: datetime) -> bool:
        """Schedule 1-hour reminder before meeting"""
        reminder_time = meeting_datetime - timedelta(hours=1)
        
        # Only schedule if reminder time is in the future
        if reminder_time > datetime.now():
            return self.schedule_reminder(lead_id, phone, name, reminder_time, "1_hour")
        else:
            logger.warning(f"1-hour reminder time {reminder_time} is in the past for lead {lead_id}")
            return False
    
    def cancel_reminders(self, lead_id: str) -> bool:
        """Cancel all reminders for a specific lead"""
        try:
            jobs = self.scheduler.get_jobs()
            cancelled_count = 0
            
            for job in jobs:
                if job.id.startswith(f"reminder_{lead_id}_"):
                    job.remove()
                    cancelled_count += 1
            
            logger.info(f"Cancelled {cancelled_count} reminders for lead {lead_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error cancelling reminders for lead {lead_id}: {str(e)}")
            return False
    
    def reschedule_reminders(self, lead_id: str, phone: str, name: str, 
                           new_meeting_datetime: datetime) -> bool:
        """Reschedule reminders for a new meeting time"""
        try:
            # Cancel existing reminders
            self.cancel_reminders(lead_id)
            
            # Schedule new reminders
            success_5h = self.schedule_5_hour_reminder(lead_id, phone, name, new_meeting_datetime)
            success_1h = self.schedule_1_hour_reminder(lead_id, phone, name, new_meeting_datetime)
            
            return success_5h and success_1h
            
        except Exception as e:
            logger.error(f"Error rescheduling reminders for lead {lead_id}: {str(e)}")
            return False
    
    def get_scheduled_reminders(self, lead_id: str = None) -> list:
        """Get all scheduled reminders or reminders for a specific lead"""
        try:
            jobs = self.scheduler.get_jobs()
            reminders = []
            
            for job in jobs:
                if job.id.startswith("reminder_"):
                    if lead_id is None or lead_id in job.id:
                        reminders.append({
                            "job_id": job.id,
                            "next_run": job.next_run_time,
                            "lead_id": job.id.split("_")[1] if len(job.id.split("_")) > 1 else None,
                            "reminder_type": job.id.split("_")[2] if len(job.id.split("_")) > 2 else None
                        })
            
            return reminders
            
        except Exception as e:
            logger.error(f"Error getting scheduled reminders: {str(e)}")
            return []
    
    def _log_reminder_sent(self, lead_id: str, phone: str, name: str, 
                          reminder_type: str, message_sid: str):
        """Log that a reminder was sent"""
        try:
            log_entry = {
                "lead_id": lead_id,
                "phone": phone,
                "name": name,
                "reminder_type": reminder_type,
                "message_sid": message_sid,
                "sent_at": datetime.now().isoformat()
            }
            
            # In production, this would be stored in a database
            logger.info(f"Reminder sent: {json.dumps(log_entry)}")
            
        except Exception as e:
            logger.error(f"Error logging reminder sent: {str(e)}")
    
    def shutdown(self):
        """Shutdown the scheduler gracefully"""
        try:
            if self.scheduler.running:
                self.scheduler.shutdown()
                logger.info("Reminder scheduler shutdown successfully")
        except Exception as e:
            logger.error(f"Error shutting down scheduler: {str(e)}")
    
    def health_check(self) -> Dict[str, Any]:
        """Check scheduler health"""
        try:
            return {
                "running": self.scheduler.running,
                "job_count": len(self.scheduler.get_jobs()),
                "next_job": self.scheduler.get_jobs()[0].next_run_time if self.scheduler.get_jobs() else None
            }
        except Exception as e:
            logger.error(f"Error in health check: {str(e)}")
            return {
                "running": False,
                "error": str(e)
            } 