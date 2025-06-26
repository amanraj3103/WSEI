#!/usr/bin/env python3
"""
Database setup script for WhatsApp Lead Assistant
"""

import os
import sqlite3
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_database():
    """Create SQLite database with necessary tables"""
    try:
        # Create data directory if it doesn't exist
        os.makedirs("data", exist_ok=True)
        
        # Connect to SQLite database
        conn = sqlite3.connect("data/leads.db")
        cursor = conn.cursor()
        
        # Create leads table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lead_id TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                email TEXT,
                phone TEXT,
                country TEXT,
                service_type TEXT,
                preferred_date TEXT,
                preferred_time TEXT,
                notes TEXT,
                source TEXT DEFAULT 'WhatsApp',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create reminders table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lead_id TEXT NOT NULL,
                reminder_type TEXT NOT NULL,
                scheduled_time TIMESTAMP NOT NULL,
                sent_time TIMESTAMP,
                status TEXT DEFAULT 'scheduled',
                message_sid TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (lead_id) REFERENCES leads (lead_id)
            )
        ''')
        
        # Create conversations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lead_id TEXT NOT NULL,
                message_sid TEXT NOT NULL,
                from_number TEXT NOT NULL,
                message_body TEXT NOT NULL,
                response_body TEXT,
                intent TEXT,
                entities TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (lead_id) REFERENCES leads (lead_id)
            )
        ''')
        
        # Create reports table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lead_id TEXT NOT NULL,
                report_type TEXT NOT NULL,
                file_path TEXT NOT NULL,
                generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                sent_to_admin BOOLEAN DEFAULT FALSE,
                FOREIGN KEY (lead_id) REFERENCES leads (lead_id)
            )
        ''')
        
        # Create indexes for better performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_leads_created_at ON leads(created_at)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_leads_service_type ON leads(service_type)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_reminders_scheduled_time ON reminders(scheduled_time)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_reminders_status ON reminders(status)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_conversations_lead_id ON conversations(lead_id)')
        
        # Commit changes
        conn.commit()
        
        logger.info("Database created successfully!")
        
        # Test the database
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        logger.info(f"Created tables: {[table[0] for table in tables]}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error creating database: {str(e)}")
        return False
    
    finally:
        if conn:
            conn.close()

def create_sample_data():
    """Create sample data for testing"""
    try:
        conn = sqlite3.connect("data/leads.db")
        cursor = conn.cursor()
        
        # Sample lead data
        sample_leads = [
            {
                "lead_id": "sample_001",
                "name": "John Doe",
                "email": "john.doe@example.com",
                "phone": "+1234567890",
                "country": "United States",
                "service_type": "study",
                "preferred_date": "tomorrow",
                "preferred_time": "2 PM",
                "notes": "Interested in studying abroad",
                "source": "WhatsApp"
            },
            {
                "lead_id": "sample_002",
                "name": "Jane Smith",
                "email": "jane.smith@example.com",
                "phone": "+1987654321",
                "country": "Canada",
                "service_type": "work",
                "preferred_date": "next Monday",
                "preferred_time": "10 AM",
                "notes": "Looking for work opportunities",
                "source": "WhatsApp"
            }
        ]
        
        for lead in sample_leads:
            cursor.execute('''
                INSERT OR IGNORE INTO leads 
                (lead_id, name, email, phone, country, service_type, preferred_date, preferred_time, notes, source)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                lead["lead_id"], lead["name"], lead["email"], lead["phone"],
                lead["country"], lead["service_type"], lead["preferred_date"],
                lead["preferred_time"], lead["notes"], lead["source"]
            ))
        
        conn.commit()
        logger.info("Sample data created successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Error creating sample data: {str(e)}")
        return False
    
    finally:
        if conn:
            conn.close()

def main():
    """Main setup function"""
    logger.info("Starting database setup...")
    
    # Create database
    if create_database():
        logger.info("Database setup completed successfully!")
        
        # Ask if user wants sample data
        try:
            response = input("Do you want to create sample data? (y/n): ").lower().strip()
            if response in ['y', 'yes']:
                create_sample_data()
        except KeyboardInterrupt:
            logger.info("Setup interrupted by user")
    else:
        logger.error("Database setup failed!")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 