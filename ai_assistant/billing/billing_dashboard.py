"""
Simple Billing Dashboard for WhatsApp Lead Assistant
Web interface for manual billing management
"""

import os
import sys
from datetime import datetime, date, timedelta
from typing import Dict, List
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import uvicorn

# Add the billing directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from manual_billing import ManualBillingManager, Customer, Payment, PRICING_PLANS

# Initialize FastAPI app
app = FastAPI(title="Billing Dashboard", version="1.0.0")

# Initialize billing manager
billing = ManualBillingManager()

# Templates (we'll use simple HTML for now)
templates = Jinja2Templates(directory="billing/templates")

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Main billing dashboard"""
    
    # Get statistics
    total_customers = len(billing.customers)
    active_customers = len([c for c in billing.customers.values() if c.is_active])
    overdue_customers = len(billing.get_overdue_customers())
    monthly_revenue = billing.get_monthly_revenue()
    
    # Get recent customers
    recent_customers = list(billing.customers.values())[-5:]  # Last 5 customers
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Billing Dashboard - WhatsApp Lead Assistant</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
            .container {{ max-width: 1200px; margin: 0 auto; }}
            .header {{ background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 20px; }}
            .stat-card {{ background: white; padding: 20px; border-radius: 8px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            .stat-number {{ font-size: 2em; font-weight: bold; color: #007bff; }}
            .stat-label {{ color: #666; margin-top: 5px; }}
            .section {{ background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            .btn {{ background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; text-decoration: none; display: inline-block; }}
            .btn:hover {{ background: #0056b3; }}
            .btn-success {{ background: #28a745; }}
            .btn-warning {{ background: #ffc107; color: black; }}
            .btn-danger {{ background: #dc3545; }}
            table {{ width: 100%; border-collapse: collapse; }}
            th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
            th {{ background-color: #f8f9fa; }}
            .status-paid {{ color: #28a745; font-weight: bold; }}
            .status-pending {{ color: #ffc107; font-weight: bold; }}
            .status-overdue {{ color: #dc3545; font-weight: bold; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>💰 Billing Dashboard</h1>
                <p>WhatsApp Lead Assistant - Manual Billing Management</p>
            </div>
            
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-number">{total_customers}</div>
                    <div class="stat-label">Total Customers</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{active_customers}</div>
                    <div class="stat-label">Active Customers</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">${monthly_revenue:.2f}</div>
                    <div class="stat-label">Monthly Revenue</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{overdue_customers}</div>
                    <div class="stat-label">Overdue Payments</div>
                </div>
            </div>
            
            <div class="section">
                <h2>Quick Actions</h2>
                <a href="/add-customer" class="btn">➕ Add New Customer</a>
                <a href="/customers" class="btn">👥 View All Customers</a>
                <a href="/payments" class="btn">💳 Record Payment</a>
                <a href="/overdue" class="btn btn-warning">⚠️ Overdue Customers</a>
                <a href="/export" class="btn btn-success">📊 Export Data</a>
            </div>
            
            <div class="section">
                <h2>Recent Customers</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Company</th>
                            <th>Plan</th>
                            <th>Monthly Price</th>
                            <th>Status</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
    """
    
    for customer in recent_customers:
        status_class = f"status-{customer.payment_status}"
        html_content += f"""
                        <tr>
                            <td>{customer.name}</td>
                            <td>{customer.company}</td>
                            <td>{customer.plan.title()}</td>
                            <td>${customer.monthly_price:.2f}</td>
                            <td class="{status_class}">{customer.payment_status.title()}</td>
                            <td>
                                <a href="/customer/{customer.customer_id}" class="btn">View</a>
                                <a href="/invoice/{customer.customer_id}" class="btn btn-success">Invoice</a>
                            </td>
                        </tr>
        """
    
    html_content += """
                    </tbody>
                </table>
            </div>
        </div>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html_content)

@app.get("/add-customer", response_class=HTMLResponse)
async def add_customer_form(request: Request):
    """Form to add a new customer"""
    
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Add Customer - Billing Dashboard</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
            .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            .form-group { margin-bottom: 20px; }
            label { display: block; margin-bottom: 5px; font-weight: bold; }
            input, select { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; }
            .btn { background: #007bff; color: white; padding: 12px 24px; border: none; border-radius: 4px; cursor: pointer; }
            .btn:hover { background: #0056b3; }
            .pricing { background: #f8f9fa; padding: 15px; border-radius: 4px; margin-bottom: 20px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>➕ Add New Customer</h1>
            
            <div class="pricing">
                <h3>Pricing Plans</h3>
                <p><strong>Basic:</strong> $29/month - 1,000 messages</p>
                <p><strong>Pro:</strong> $79/month - 5,000 messages</p>
                <p><strong>Enterprise:</strong> $199/month - 20,000 messages</p>
            </div>
            
            <form method="POST" action="/add-customer">
                <div class="form-group">
                    <label>Customer ID:</label>
                    <input type="text" name="customer_id" required placeholder="e.g., CUST001">
                </div>
                
                <div class="form-group">
                    <label>Name:</label>
                    <input type="text" name="name" required placeholder="Full name">
                </div>
                
                <div class="form-group">
                    <label>Email:</label>
                    <input type="email" name="email" required placeholder="email@example.com">
                </div>
                
                <div class="form-group">
                    <label>Company:</label>
                    <input type="text" name="company" required placeholder="Company name">
                </div>
                
                <div class="form-group">
                    <label>Phone:</label>
                    <input type="text" name="phone" placeholder="+1234567890">
                </div>
                
                <div class="form-group">
                    <label>Plan:</label>
                    <select name="plan" required>
                        <option value="basic">Basic ($29/month)</option>
                        <option value="pro">Pro ($79/month)</option>
                        <option value="enterprise">Enterprise ($199/month)</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label>Start Date:</label>
                    <input type="date" name="start_date" required>
                </div>
                
                <div class="form-group">
                    <label>Billing Cycle:</label>
                    <select name="billing_cycle" required>
                        <option value="monthly">Monthly</option>
                        <option value="quarterly">Quarterly</option>
                        <option value="yearly">Yearly</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label>Notes:</label>
                    <input type="text" name="notes" placeholder="Additional notes">
                </div>
                
                <button type="submit" class="btn">Add Customer</button>
                <a href="/" style="margin-left: 10px;">Cancel</a>
            </form>
        </div>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html_content)

@app.post("/add-customer")
async def add_customer(
    customer_id: str = Form(...),
    name: str = Form(...),
    email: str = Form(...),
    company: str = Form(...),
    phone: str = Form(...),
    plan: str = Form(...),
    start_date: str = Form(...),
    billing_cycle: str = Form(...),
    notes: str = Form("")
):
    """Add a new customer"""
    
    # Get plan price
    plan_price = PRICING_PLANS[plan]["price"]
    
    # Calculate next payment date
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    if billing_cycle == "monthly":
        next_payment = start_dt.replace(day=1) + timedelta(days=32)
        next_payment = next_payment.replace(day=1)
    elif billing_cycle == "quarterly":
        next_payment = start_dt.replace(month=start_dt.month + 3)
    else:  # yearly
        next_payment = start_dt.replace(year=start_dt.year + 1)
    
    customer = Customer(
        customer_id=customer_id,
        name=name,
        email=email,
        company=company,
        phone=phone,
        plan=plan,
        monthly_price=plan_price,
        start_date=start_date,
        billing_cycle=billing_cycle,
        payment_status="pending",
        next_payment_date=next_payment.strftime("%Y-%m-%d"),
        notes=notes
    )
    
    billing.add_customer(customer)
    return RedirectResponse(url="/", status_code=303)

@app.get("/customers", response_class=HTMLResponse)
async def list_customers(request: Request):
    """List all customers"""
    
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>All Customers - Billing Dashboard</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
            .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            table { width: 100%; border-collapse: collapse; }
            th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
            th { background-color: #f8f9fa; }
            .btn { background: #007bff; color: white; padding: 8px 16px; border: none; border-radius: 4px; cursor: pointer; text-decoration: none; display: inline-block; margin: 2px; }
            .status-paid { color: #28a745; font-weight: bold; }
            .status-pending { color: #ffc107; font-weight: bold; }
            .status-overdue { color: #dc3545; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>👥 All Customers</h1>
            <a href="/" class="btn">← Back to Dashboard</a>
            
            <table>
                <thead>
                    <tr>
                        <th>Customer ID</th>
                        <th>Name</th>
                        <th>Company</th>
                        <th>Email</th>
                        <th>Plan</th>
                        <th>Monthly Price</th>
                        <th>Status</th>
                        <th>Next Payment</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
    """
    
    for customer in billing.customers.values():
        status_class = f"status-{customer.payment_status}"
        html_content += f"""
                    <tr>
                        <td>{customer.customer_id}</td>
                        <td>{customer.name}</td>
                        <td>{customer.company}</td>
                        <td>{customer.email}</td>
                        <td>{customer.plan.title()}</td>
                        <td>${customer.monthly_price:.2f}</td>
                        <td class="{status_class}">{customer.payment_status.title()}</td>
                        <td>{customer.next_payment_date or 'N/A'}</td>
                        <td>
                            <a href="/customer/{customer.customer_id}" class="btn">View</a>
                            <a href="/invoice/{customer.customer_id}" class="btn">Invoice</a>
                        </td>
                    </tr>
        """
    
    html_content += """
                </tbody>
            </table>
        </div>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html_content)

@app.get("/invoice/{customer_id}", response_class=HTMLResponse)
async def generate_invoice(customer_id: str):
    """Generate invoice for a customer"""
    
    invoice = billing.generate_invoice(customer_id)
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Invoice - Billing Dashboard</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
            .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            .invoice {{ font-family: monospace; white-space: pre-line; background: #f8f9fa; padding: 20px; border-radius: 4px; }}
            .btn {{ background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; text-decoration: none; display: inline-block; margin: 10px 5px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📄 Invoice</h1>
            <a href="/" class="btn">← Back to Dashboard</a>
            <a href="/customers" class="btn">View All Customers</a>
            
            <div class="invoice">{invoice}</div>
            
            <div style="margin-top: 20px;">
                <button onclick="window.print()" class="btn">🖨️ Print Invoice</button>
                <button onclick="navigator.clipboard.writeText(document.querySelector('.invoice').textContent)" class="btn">📋 Copy to Clipboard</button>
            </div>
        </div>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html_content)

@app.get("/export")
async def export_data():
    """Export customer data to CSV"""
    
    filename = f"customers_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    billing.export_customers_csv(filename)
    
    return RedirectResponse(url="/", status_code=303)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001) 