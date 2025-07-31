"""
Manual Billing System for WhatsApp Lead Assistant
Simple tracking system for manual billing
"""

import json
import os
from datetime import datetime, date
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import csv

@dataclass
class Customer:
    """Customer information for manual billing"""
    customer_id: str
    name: str
    email: str
    company: str
    phone: str
    plan: str  # 'basic', 'pro', 'enterprise'
    monthly_price: float
    start_date: str
    billing_cycle: str  # 'monthly', 'quarterly', 'yearly'
    payment_status: str  # 'paid', 'pending', 'overdue'
    last_payment_date: Optional[str] = None
    next_payment_date: Optional[str] = None
    notes: str = ""
    is_active: bool = True

@dataclass
class Payment:
    """Payment record"""
    payment_id: str
    customer_id: str
    amount: float
    payment_date: str
    payment_method: str  # 'bank_transfer', 'paypal', 'cash', 'other'
    reference: str
    status: str  # 'received', 'pending', 'failed'
    notes: str = ""

class ManualBillingManager:
    """Manages manual billing for customers"""
    
    def __init__(self, data_dir: str = "billing_data"):
        self.data_dir = data_dir
        self.customers_file = os.path.join(data_dir, "customers.json")
        self.payments_file = os.path.join(data_dir, "payments.json")
        
        # Create data directory if it doesn't exist
        os.makedirs(data_dir, exist_ok=True)
        
        # Load existing data
        self.customers = self.load_customers()
        self.payments = self.load_payments()
    
    def load_customers(self) -> Dict[str, Customer]:
        """Load customers from JSON file"""
        if os.path.exists(self.customers_file):
            with open(self.customers_file, 'r') as f:
                data = json.load(f)
                return {k: Customer(**v) for k, v in data.items()}
        return {}
    
    def save_customers(self):
        """Save customers to JSON file"""
        with open(self.customers_file, 'w') as f:
            data = {k: asdict(v) for k, v in self.customers.items()}
            json.dump(data, f, indent=2)
    
    def load_payments(self) -> List[Payment]:
        """Load payments from JSON file"""
        if os.path.exists(self.payments_file):
            with open(self.payments_file, 'r') as f:
                data = json.load(f)
                return [Payment(**p) for p in data]
        return []
    
    def save_payments(self):
        """Save payments to JSON file"""
        with open(self.payments_file, 'w') as f:
            data = [asdict(p) for p in self.payments]
            json.dump(data, f, indent=2)
    
    def add_customer(self, customer: Customer):
        """Add a new customer"""
        self.customers[customer.customer_id] = customer
        self.save_customers()
        print(f"✅ Customer {customer.name} added successfully!")
    
    def update_customer(self, customer_id: str, **kwargs):
        """Update customer information"""
        if customer_id in self.customers:
            customer = self.customers[customer_id]
            for key, value in kwargs.items():
                if hasattr(customer, key):
                    setattr(customer, key, value)
            self.save_customers()
            print(f"✅ Customer {customer.name} updated successfully!")
        else:
            print(f"❌ Customer {customer_id} not found!")
    
    def record_payment(self, payment: Payment):
        """Record a payment"""
        self.payments.append(payment)
        self.save_payments()
        
        # Update customer payment status
        if payment.customer_id in self.customers:
            customer = self.customers[payment.customer_id]
            customer.payment_status = "paid"
            customer.last_payment_date = payment.payment_date
            self.save_customers()
        
        print(f"✅ Payment of ${payment.amount} recorded for customer {payment.customer_id}!")
    
    def get_overdue_customers(self) -> List[Customer]:
        """Get customers with overdue payments"""
        overdue = []
        today = date.today()
        
        for customer in self.customers.values():
            if customer.next_payment_date:
                next_payment = datetime.strptime(customer.next_payment_date, "%Y-%m-%d").date()
                if next_payment < today and customer.payment_status != "paid":
                    overdue.append(customer)
        
        return overdue
    
    def get_monthly_revenue(self, month: str = None) -> float:
        """Calculate monthly revenue"""
        if month is None:
            month = datetime.now().strftime("%Y-%m")
        
        total = 0
        for customer in self.customers.values():
            if customer.is_active and customer.payment_status == "paid":
                # Simple calculation - in real scenario, check actual payment dates
                total += customer.monthly_price
        
        return total
    
    def generate_invoice(self, customer_id: str) -> str:
        """Generate a simple invoice for a customer"""
        if customer_id not in self.customers:
            return "Customer not found!"
        
        customer = self.customers[customer_id]
        invoice_number = f"INV-{customer_id}-{datetime.now().strftime('%Y%m%d')}"
        
        invoice = f"""
INVOICE
========

Invoice Number: {invoice_number}
Date: {datetime.now().strftime('%Y-%m-%d')}

Bill To:
{customer.name}
{customer.company}
{customer.email}

Service: WhatsApp Lead Assistant - {customer.plan.title()} Plan
Amount: ${customer.monthly_price:.2f}

Payment Terms: Due upon receipt
Payment Methods: Bank Transfer, PayPal, Cash

Thank you for your business!
        """
        
        return invoice
    
    def export_customers_csv(self, filename: str = "customers.csv"):
        """Export customers to CSV file"""
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Customer ID', 'Name', 'Email', 'Company', 'Plan', 'Monthly Price', 'Status'])
            
            for customer in self.customers.values():
                writer.writerow([
                    customer.customer_id,
                    customer.name,
                    customer.email,
                    customer.company,
                    customer.plan,
                    customer.monthly_price,
                    customer.payment_status
                ])
        
        print(f"✅ Customers exported to {filename}")

# Pricing plans
PRICING_PLANS = {
    "basic": {
        "price": 29.00,
        "messages": 1000,
        "features": ["WhatsApp webhook", "Basic responses", "Email support"]
    },
    "pro": {
        "price": 79.00,
        "messages": 5000,
        "features": ["WhatsApp webhook", "Advanced responses", "HubSpot integration", "Priority support"]
    },
    "enterprise": {
        "price": 199.00,
        "messages": 20000,
        "features": ["Everything in Pro", "Custom integrations", "Dedicated support", "Custom features"]
    }
}

# Example usage
if __name__ == "__main__":
    # Initialize billing manager
    billing = ManualBillingManager()
    
    # Example: Add a customer
    customer = Customer(
        customer_id="CUST001",
        name="John Smith",
        email="john@example.com",
        company="Smith Consulting",
        phone="+1234567890",
        plan="basic",
        monthly_price=29.00,
        start_date="2024-01-01",
        billing_cycle="monthly",
        payment_status="pending",
        next_payment_date="2024-02-01"
    )
    
    billing.add_customer(customer)
    
    # Example: Record a payment
    payment = Payment(
        payment_id="PAY001",
        customer_id="CUST001",
        amount=29.00,
        payment_date="2024-01-15",
        payment_method="bank_transfer",
        reference="TRX123456",
        status="received"
    )
    
    billing.record_payment(payment)
    
    # Generate invoice
    invoice = billing.generate_invoice("CUST001")
    print(invoice)
    
    # Export customers
    billing.export_customers_csv() 