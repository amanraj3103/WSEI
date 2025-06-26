import os
import logging
import requests
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class HubSpotClient:
    """Client for interacting with HubSpot CRM API"""
    
    def __init__(self):
        self.api_key = os.getenv('HUBSPOT_API_KEY')
        self.portal_id = os.getenv('HUBSPOT_PORTAL_ID')
        self.base_url = "https://api.hubapi.com"
        
        if not self.api_key:
            logger.error("HUBSPOT_API_KEY not found in environment variables")
            raise ValueError("HUBSPOT_API_KEY is required")
        
        if not self.portal_id:
            logger.error("HUBSPOT_PORTAL_ID not found in environment variables")
            raise ValueError("HUBSPOT_PORTAL_ID is required")
    
    def create_lead(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new lead in HubSpot CRM"""
        try:
            # Prepare contact properties
            properties = {
                "email": lead_data.get("email", ""),
                "firstname": self._extract_first_name(lead_data.get("name", "")),
                "lastname": self._extract_last_name(lead_data.get("name", "")),
                "phone": lead_data.get("phone", ""),
                "country": lead_data.get("country", ""),
                "service_type": lead_data.get("service_type", ""),
                "preferred_date": lead_data.get("preferred_date", ""),
                "preferred_time": lead_data.get("preferred_time", ""),
                "notes": lead_data.get("notes", ""),
                "lead_source": "WhatsApp",
                "createdate": str(int(datetime.now().timestamp() * 1000))
            }
            
            # Create contact
            contact_response = self._create_contact(properties)
            
            if contact_response.get("success"):
                contact_id = contact_response.get("contact_id")
                
                # Create deal/opportunity
                deal_response = self._create_deal(contact_id, lead_data)
                
                # Create note with additional information
                self._create_note(contact_id, lead_data)
                
                return {
                    "success": True,
                    "lead_id": contact_id,
                    "contact_id": contact_id,
                    "deal_id": deal_response.get("deal_id") if deal_response.get("success") else None
                }
            else:
                return {
                    "success": False,
                    "error": contact_response.get("error", "Failed to create contact")
                }
                
        except Exception as e:
            logger.error(f"Error creating lead in HubSpot: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _create_contact(self, properties: Dict[str, str]) -> Dict[str, Any]:
        """Create a new contact in HubSpot"""
        try:
            url = f"{self.base_url}/crm/v3/objects/contacts"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "properties": properties
            }
            
            response = requests.post(url, headers=headers, json=payload)
            
            if response.status_code == 201:
                contact_data = response.json()
                return {
                    "success": True,
                    "contact_id": contact_data.get("id")
                }
            else:
                logger.error(f"HubSpot API error: {response.status_code} - {response.text}")
                return {
                    "success": False,
                    "error": f"API error: {response.status_code}"
                }
                
        except Exception as e:
            logger.error(f"Error creating contact: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _create_deal(self, contact_id: str, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a deal/opportunity for the contact"""
        try:
            url = f"{self.base_url}/crm/v3/objects/deals"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # Map service type to deal stage
            stage_mapping = {
                "study": "appointmentscheduled",
                "work": "appointmentscheduled",
                "visa_help": "appointmentscheduled"
            }
            
            properties = {
                "dealname": f"Consultation - {lead_data.get('name', 'Unknown')}",
                "dealstage": stage_mapping.get(lead_data.get("service_type", ""), "appointmentscheduled"),
                "amount": "0",
                "pipeline": "default",
                "service_type": lead_data.get("service_type", ""),
                "country_of_interest": lead_data.get("country", ""),
                "createdate": str(int(datetime.now().timestamp() * 1000))
            }
            
            payload = {
                "properties": properties,
                "associations": [
                    {
                        "to": {
                            "id": contact_id
                        },
                        "types": [
                            {
                                "associationCategory": "HUBSPOT_DEFINED",
                                "associationTypeId": 3
                            }
                        ]
                    }
                ]
            }
            
            response = requests.post(url, headers=headers, json=payload)
            
            if response.status_code == 201:
                deal_data = response.json()
                return {
                    "success": True,
                    "deal_id": deal_data.get("id")
                }
            else:
                logger.error(f"HubSpot API error creating deal: {response.status_code} - {response.text}")
                return {
                    "success": False,
                    "error": f"API error: {response.status_code}"
                }
                
        except Exception as e:
            logger.error(f"Error creating deal: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _create_note(self, contact_id: str, lead_data: Dict[str, Any]) -> bool:
        """Create a note with additional lead information"""
        try:
            url = f"{self.base_url}/crm/v3/objects/notes"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            note_content = f"""
Lead Information:
- Name: {lead_data.get('name', 'N/A')}
- Service Type: {lead_data.get('service_type', 'N/A')}
- Country: {lead_data.get('country', 'N/A')}
- Preferred Date: {lead_data.get('preferred_date', 'N/A')}
- Preferred Time: {lead_data.get('preferred_time', 'N/A')}
- Notes: {lead_data.get('notes', 'N/A')}
- Source: WhatsApp Lead Assistant
- Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            """.strip()
            
            payload = {
                "properties": {
                    "hs_note_body": note_content,
                    "hs_timestamp": str(int(datetime.now().timestamp() * 1000))
                },
                "associations": [
                    {
                        "to": {
                            "id": contact_id
                        },
                        "types": [
                            {
                                "associationCategory": "HUBSPOT_DEFINED",
                                "associationTypeId": 1
                            }
                        ]
                    }
                ]
            }
            
            response = requests.post(url, headers=headers, json=payload)
            return response.status_code == 201
            
        except Exception as e:
            logger.error(f"Error creating note: {str(e)}")
            return False
    
    def _extract_first_name(self, full_name: str) -> str:
        """Extract first name from full name"""
        if not full_name:
            return ""
        return full_name.split()[0] if " " in full_name else full_name
    
    def _extract_last_name(self, full_name: str) -> str:
        """Extract last name from full name"""
        if not full_name or " " not in full_name:
            return ""
        return " ".join(full_name.split()[1:])
    
    def get_contact(self, contact_id: str) -> Optional[Dict[str, Any]]:
        """Get contact information from HubSpot"""
        try:
            url = f"{self.base_url}/crm/v3/objects/contacts/{contact_id}"
            headers = {
                "Authorization": f"Bearer {self.api_key}"
            }
            
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Error getting contact: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting contact: {str(e)}")
            return None 