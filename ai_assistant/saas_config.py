"""
SaaS Configuration for WhatsApp Lead Assistant
Multi-tenant setup for selling as SaaS software
"""

import os
from typing import Dict, Any
from dataclasses import dataclass
from datetime import datetime

@dataclass
class TenantConfig:
    """Configuration for each SaaS tenant"""
    tenant_id: str
    name: str
    twilio_account_sid: str
    twilio_auth_token: str
    twilio_phone_number: str
    hubspot_api_key: str
    hubspot_portal_id: str
    calendly_api_key: str
    calendly_user_uri: str
    encryption_key: str
    plan: str  # 'basic', 'pro', 'enterprise'
    monthly_limit: int  # messages per month
    features: list  # enabled features
    created_at: datetime
    is_active: bool = True

class SaaSManager:
    """Manages multiple tenants for SaaS deployment"""
    
    def __init__(self):
        self.tenants: Dict[str, TenantConfig] = {}
        self.load_tenants()
    
    def load_tenants(self):
        """Load tenant configurations from environment or database"""
        # For now, load from environment variables
        # In production, this would be a database
        default_tenant = TenantConfig(
            tenant_id="default",
            name="Default Tenant",
            twilio_account_sid=os.getenv("TWILIO_ACCOUNT_SID", ""),
            twilio_auth_token=os.getenv("TWILIO_AUTH_TOKEN", ""),
            twilio_phone_number=os.getenv("TWILIO_PHONE_NUMBER", ""),
            hubspot_api_key=os.getenv("HUBSPOT_API_KEY", ""),
            hubspot_portal_id=os.getenv("HUBSPOT_PORTAL_ID", ""),
            calendly_api_key=os.getenv("CALENDLY_API_KEY", ""),
            calendly_user_uri=os.getenv("CALENDLY_USER_URI", ""),
            encryption_key=os.getenv("ENCRYPTION_KEY", ""),
            plan="basic",
            monthly_limit=1000,
            features=["webhook", "basic_responses", "health_check"],
            created_at=datetime.now()
        )
        self.tenants["default"] = default_tenant
    
    def get_tenant(self, tenant_id: str) -> TenantConfig:
        """Get tenant configuration by ID"""
        return self.tenants.get(tenant_id, self.tenants["default"])
    
    def add_tenant(self, config: TenantConfig):
        """Add a new tenant"""
        self.tenants[config.tenant_id] = config
    
    def check_usage_limit(self, tenant_id: str, current_usage: int) -> bool:
        """Check if tenant has exceeded monthly limit"""
        tenant = self.get_tenant(tenant_id)
        return current_usage < tenant.monthly_limit

# SaaS Pricing Plans
SAAS_PLANS = {
    "basic": {
        "price": 29,
        "monthly_messages": 1000,
        "features": ["webhook", "basic_responses", "health_check", "email_support"],
        "description": "Perfect for small businesses"
    },
    "pro": {
        "price": 79,
        "monthly_messages": 5000,
        "features": ["webhook", "rasa_nlp", "hubspot_integration", "calendly_integration", "priority_support"],
        "description": "For growing businesses with advanced features"
    },
    "enterprise": {
        "price": 199,
        "monthly_messages": 20000,
        "features": ["webhook", "rasa_nlp", "hubspot_integration", "calendly_integration", "custom_integrations", "dedicated_support"],
        "description": "For large enterprises with custom needs"
    }
}

# Usage tracking
class UsageTracker:
    """Track usage for billing and limits"""
    
    def __init__(self):
        self.usage = {}  # tenant_id -> monthly_usage
    
    def increment_usage(self, tenant_id: str):
        """Increment monthly usage for tenant"""
        if tenant_id not in self.usage:
            self.usage[tenant_id] = 0
        self.usage[tenant_id] += 1
    
    def get_usage(self, tenant_id: str) -> int:
        """Get current monthly usage for tenant"""
        return self.usage.get(tenant_id, 0)
    
    def reset_monthly_usage(self):
        """Reset usage at start of month (call via cron job)"""
        self.usage = {}

# Initialize global instances
saas_manager = SaaSManager()
usage_tracker = UsageTracker() 