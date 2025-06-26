import os
import logging
import requests
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class CalendlyClient:
    """Client for interacting with Calendly API"""
    
    def __init__(self):
        self.api_key = os.getenv('CALENDLY_API_KEY')
        self.user_uri = os.getenv('CALENDLY_USER_URI')
        self.base_url = "https://api.calendly.com"
        
        if not self.api_key:
            logger.error("CALENDLY_API_KEY not found in environment variables")
            raise ValueError("CALENDLY_API_KEY is required")
        
        if not self.user_uri:
            logger.error("CALENDLY_USER_URI not found in environment variables")
            raise ValueError("CALENDLY_USER_URI is required")
    
    def create_booking_link(self, name: str, service_type: str, country: str) -> Optional[str]:
        """Create a personalized Calendly booking link"""
        try:
            # Get available event types
            event_types = self._get_event_types()
            
            if not event_types:
                logger.error("No event types found in Calendly")
                return None
            
            # Select appropriate event type based on service
            event_type_uri = self._select_event_type(event_types, service_type)
            
            if not event_type_uri:
                logger.error(f"No suitable event type found for service: {service_type}")
                return None
            
            # Create scheduling link
            scheduling_link = self._create_scheduling_link(event_type_uri, name, service_type, country)
            
            return scheduling_link
            
        except Exception as e:
            logger.error(f"Error creating booking link: {str(e)}")
            return None
    
    def _get_event_types(self) -> list:
        """Get available event types from Calendly"""
        try:
            url = f"{self.base_url}/event_types"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            params = {
                "user": self.user_uri,
                "active": "true"
            }
            
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                return data.get("collection", [])
            else:
                logger.error(f"Calendly API error: {response.status_code} - {response.text}")
                return []
                
        except Exception as e:
            logger.error(f"Error getting event types: {str(e)}")
            return []
    
    def _select_event_type(self, event_types: list, service_type: str) -> Optional[str]:
        """Select the most appropriate event type based on service"""
        try:
            # Map service types to event type names/keywords
            service_mapping = {
                "study": ["study", "education", "consultation", "meeting"],
                "work": ["work", "employment", "consultation", "meeting"],
                "visa_help": ["visa", "immigration", "consultation", "meeting"]
            }
            
            keywords = service_mapping.get(service_type, ["consultation", "meeting"])
            
            # Find event type that matches keywords
            for event_type in event_types:
                event_name = event_type.get("name", "").lower()
                event_description = event_type.get("description", "").lower()
                
                for keyword in keywords:
                    if keyword in event_name or keyword in event_description:
                        return event_type.get("uri")
            
            # If no specific match, return the first available event type
            if event_types:
                return event_types[0].get("uri")
            
            return None
            
        except Exception as e:
            logger.error(f"Error selecting event type: {str(e)}")
            return None
    
    def _create_scheduling_link(self, event_type_uri: str, name: str, service_type: str, country: str) -> Optional[str]:
        """Create a scheduling link with custom parameters"""
        try:
            # Extract event type slug from URI
            event_type_slug = event_type_uri.split("/")[-1]
            
            # Create base scheduling link
            base_link = f"https://calendly.com/{self.user_uri.split('/')[-1]}/{event_type_slug}"
            
            # Add custom parameters
            params = {
                "name": name,
                "service_type": service_type,
                "country": country,
                "utm_source": "whatsapp",
                "utm_medium": "chatbot",
                "utm_campaign": "lead_assistant"
            }
            
            # Build URL with parameters
            param_string = "&".join([f"{k}={v}" for k, v in params.items() if v])
            scheduling_link = f"{base_link}?{param_string}"
            
            return scheduling_link
            
        except Exception as e:
            logger.error(f"Error creating scheduling link: {str(e)}")
            return None
    
    def create_scheduled_event(self, event_type_uri: str, invitee_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a scheduled event directly via API"""
        try:
            url = f"{self.base_url}/scheduling_links"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "max_event_count": 1,
                "owner": self.user_uri,
                "owner_type": "EventType",
                "event_type": event_type_uri
            }
            
            response = requests.post(url, headers=headers, json=payload)
            
            if response.status_code == 201:
                data = response.json()
                return {
                    "success": True,
                    "booking_link": data.get("booking_url"),
                    "scheduling_link_id": data.get("resource", {}).get("uri")
                }
            else:
                logger.error(f"Calendly API error: {response.status_code} - {response.text}")
                return {
                    "success": False,
                    "error": f"API error: {response.status_code}"
                }
                
        except Exception as e:
            logger.error(f"Error creating scheduled event: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_user_info(self) -> Optional[Dict[str, Any]]:
        """Get Calendly user information"""
        try:
            url = f"{self.base_url}/users/{self.user_uri.split('/')[-1]}"
            headers = {
                "Authorization": f"Bearer {self.api_key}"
            }
            
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Error getting user info: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting user info: {str(e)}")
            return None
    
    def get_scheduled_events(self, start_time: datetime = None, end_time: datetime = None) -> list:
        """Get scheduled events within a time range"""
        try:
            url = f"{self.base_url}/scheduled_events"
            headers = {
                "Authorization": f"Bearer {self.api_key}"
            }
            
            params = {
                "user": self.user_uri
            }
            
            if start_time:
                params["min_start_time"] = start_time.isoformat()
            
            if end_time:
                params["max_start_time"] = end_time.isoformat()
            
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                return data.get("collection", [])
            else:
                logger.error(f"Error getting scheduled events: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Error getting scheduled events: {str(e)}")
            return [] 