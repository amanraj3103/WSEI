import os
import logging
import json
from datetime import datetime
from typing import Dict, Any, Optional, List
import pandas as pd
from fpdf import FPDF
import xlsxwriter

from integrations.hubspot.hubspot_client import HubSpotClient
from integrations.encryption.encryption_utils import EncryptionUtils

logger = logging.getLogger(__name__)

class ReportGenerator:
    """Generate PDF and Excel reports for lead conversations"""
    
    def __init__(self):
        self.hubspot_client = HubSpotClient()
        self.encryption_utils = EncryptionUtils()
        self.reports_dir = "reports"
        
        # Create reports directory if it doesn't exist
        if not os.path.exists(self.reports_dir):
            os.makedirs(self.reports_dir)
    
    def generate_lead_report(self, lead_id: str, report_type: str = "both") -> Optional[str]:
        """Generate report for a specific lead"""
        try:
            # Get lead data from HubSpot
            lead_data = self._get_lead_data(lead_id)
            
            if not lead_data:
                logger.error(f"No lead data found for ID: {lead_id}")
                return None
            
            report_paths = []
            
            if report_type in ["pdf", "both"]:
                pdf_path = self._generate_pdf_report(lead_data, lead_id)
                if pdf_path:
                    report_paths.append(pdf_path)
            
            if report_type in ["excel", "both"]:
                excel_path = self._generate_excel_report(lead_data, lead_id)
                if excel_path:
                    report_paths.append(excel_path)
            
            # Send report to admin
            if report_paths:
                self._send_report_to_admin(report_paths, lead_data)
            
            return report_paths[0] if report_paths else None
            
        except Exception as e:
            logger.error(f"Error generating lead report: {str(e)}")
            return None
    
    def generate_daily_report(self, date: datetime = None) -> Optional[str]:
        """Generate daily summary report"""
        try:
            if date is None:
                date = datetime.now()
            
            # Get all leads for the day
            leads_data = self._get_leads_for_date(date)
            
            if not leads_data:
                logger.info(f"No leads found for date: {date.strftime('%Y-%m-%d')}")
                return None
            
            # Generate summary report
            report_path = self._generate_summary_report(leads_data, date)
            
            if report_path:
                self._send_report_to_admin([report_path], {"date": date.strftime('%Y-%m-%d')})
            
            return report_path
            
        except Exception as e:
            logger.error(f"Error generating daily report: {str(e)}")
            return None
    
    def _get_lead_data(self, lead_id: str) -> Optional[Dict[str, Any]]:
        """Get lead data from HubSpot"""
        try:
            contact_data = self.hubspot_client.get_contact(lead_id)
            
            if not contact_data:
                return None
            
            # Extract and decrypt sensitive data
            properties = contact_data.get("properties", {})
            
            lead_data = {
                "id": lead_id,
                "name": f"{properties.get('firstname', '')} {properties.get('lastname', '')}".strip(),
                "email": self.encryption_utils.decrypt(properties.get("email", "")),
                "phone": self.encryption_utils.decrypt(properties.get("phone", "")),
                "country": properties.get("country", ""),
                "service_type": properties.get("service_type", ""),
                "preferred_date": properties.get("preferred_date", ""),
                "preferred_time": properties.get("preferred_time", ""),
                "notes": properties.get("notes", ""),
                "created_at": properties.get("createdate", ""),
                "source": properties.get("lead_source", "WhatsApp")
            }
            
            return lead_data
            
        except Exception as e:
            logger.error(f"Error getting lead data: {str(e)}")
            return None
    
    def _generate_pdf_report(self, lead_data: Dict[str, Any], lead_id: str) -> Optional[str]:
        """Generate PDF report for lead"""
        try:
            pdf = FPDF()
            pdf.add_page()
            
            # Set font
            pdf.set_font("Arial", "B", 16)
            
            # Title
            pdf.cell(0, 10, "Lead Report", ln=True, align="C")
            pdf.ln(10)
            
            # Lead Information
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 10, "Lead Information", ln=True)
            pdf.ln(5)
            
            pdf.set_font("Arial", "", 10)
            
            # Basic details
            details = [
                ("Lead ID", lead_id),
                ("Name", lead_data.get("name", "N/A")),
                ("Email", lead_data.get("email", "N/A")),
                ("Phone", lead_data.get("phone", "N/A")),
                ("Country", lead_data.get("country", "N/A")),
                ("Service Type", lead_data.get("service_type", "N/A")),
                ("Preferred Date", lead_data.get("preferred_date", "N/A")),
                ("Preferred Time", lead_data.get("preferred_time", "N/A")),
                ("Source", lead_data.get("source", "N/A")),
                ("Created At", lead_data.get("created_at", "N/A"))
            ]
            
            for label, value in details:
                pdf.cell(50, 8, f"{label}:", ln=False)
                pdf.cell(0, 8, str(value), ln=True)
            
            # Notes section
            if lead_data.get("notes"):
                pdf.ln(10)
                pdf.set_font("Arial", "B", 12)
                pdf.cell(0, 10, "Additional Notes", ln=True)
                pdf.ln(5)
                
                pdf.set_font("Arial", "", 10)
                notes = lead_data.get("notes", "")
                # Wrap text for PDF
                pdf.multi_cell(0, 8, notes)
            
            # Footer
            pdf.ln(20)
            pdf.set_font("Arial", "I", 8)
            pdf.cell(0, 10, f"Report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align="C")
            
            # Save PDF
            filename = f"lead_report_{lead_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            filepath = os.path.join(self.reports_dir, filename)
            pdf.output(filepath)
            
            logger.info(f"PDF report generated: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Error generating PDF report: {str(e)}")
            return None
    
    def _generate_excel_report(self, lead_data: Dict[str, Any], lead_id: str) -> Optional[str]:
        """Generate Excel report for lead"""
        try:
            filename = f"lead_report_{lead_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            filepath = os.path.join(self.reports_dir, filename)
            
            # Create Excel workbook
            workbook = xlsxwriter.Workbook(filepath)
            
            # Add formats
            header_format = workbook.add_format({
                'bold': True,
                'bg_color': '#4F81BD',
                'font_color': 'white',
                'border': 1
            })
            
            data_format = workbook.add_format({
                'border': 1,
                'text_wrap': True
            })
            
            # Create worksheet
            worksheet = workbook.add_worksheet("Lead Information")
            
            # Set column widths
            worksheet.set_column('A:A', 20)
            worksheet.set_column('B:B', 40)
            
            # Add headers
            headers = ["Field", "Value"]
            for col, header in enumerate(headers):
                worksheet.write(0, col, header, header_format)
            
            # Add data
            data = [
                ("Lead ID", lead_id),
                ("Name", lead_data.get("name", "N/A")),
                ("Email", lead_data.get("email", "N/A")),
                ("Phone", lead_data.get("phone", "N/A")),
                ("Country", lead_data.get("country", "N/A")),
                ("Service Type", lead_data.get("service_type", "N/A")),
                ("Preferred Date", lead_data.get("preferred_date", "N/A")),
                ("Preferred Time", lead_data.get("preferred_time", "N/A")),
                ("Source", lead_data.get("source", "N/A")),
                ("Created At", lead_data.get("created_at", "N/A")),
                ("Notes", lead_data.get("notes", "N/A"))
            ]
            
            for row, (field, value) in enumerate(data, start=1):
                worksheet.write(row, 0, field, data_format)
                worksheet.write(row, 1, str(value), data_format)
            
            # Add summary sheet
            summary_sheet = workbook.add_worksheet("Summary")
            summary_sheet.write(0, 0, "Report Summary", header_format)
            summary_sheet.write(1, 0, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            summary_sheet.write(2, 0, f"Lead ID: {lead_id}")
            summary_sheet.write(3, 0, f"Service Type: {lead_data.get('service_type', 'N/A')}")
            summary_sheet.write(4, 0, f"Country: {lead_data.get('country', 'N/A')}")
            
            workbook.close()
            
            logger.info(f"Excel report generated: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Error generating Excel report: {str(e)}")
            return None
    
    def _generate_summary_report(self, leads_data: List[Dict[str, Any]], date: datetime) -> Optional[str]:
        """Generate summary report for multiple leads"""
        try:
            filename = f"daily_summary_{date.strftime('%Y%m%d')}.xlsx"
            filepath = os.path.join(self.reports_dir, filename)
            
            # Create DataFrame
            df = pd.DataFrame(leads_data)
            
            # Create Excel writer
            with pd.ExcelWriter(filepath, engine='xlsxwriter') as writer:
                # Write main data
                df.to_excel(writer, sheet_name='Leads', index=False)
                
                # Get workbook and worksheet
                workbook = writer.book
                worksheet = writer.sheets['Leads']
                
                # Add formats
                header_format = workbook.add_format({
                    'bold': True,
                    'bg_color': '#4F81BD',
                    'font_color': 'white',
                    'border': 1
                })
                
                # Format headers
                for col_num, value in enumerate(df.columns.values):
                    worksheet.write(0, col_num, value, header_format)
                
                # Add summary statistics
                summary_sheet = workbook.add_worksheet('Summary')
                
                # Service type breakdown
                service_counts = df['service_type'].value_counts()
                summary_sheet.write(0, 0, "Service Type Breakdown", header_format)
                summary_sheet.write(1, 0, "Service Type")
                summary_sheet.write(1, 1, "Count")
                
                for i, (service, count) in enumerate(service_counts.items(), start=2):
                    summary_sheet.write(i, 0, service)
                    summary_sheet.write(i, 1, count)
                
                # Country breakdown
                country_counts = df['country'].value_counts()
                summary_sheet.write(0, 3, "Country Breakdown", header_format)
                summary_sheet.write(1, 3, "Country")
                summary_sheet.write(1, 4, "Count")
                
                for i, (country, count) in enumerate(country_counts.items(), start=2):
                    summary_sheet.write(i, 3, country)
                    summary_sheet.write(i, 4, count)
                
                # Total leads
                summary_sheet.write(0, 6, "Total Leads", header_format)
                summary_sheet.write(1, 6, len(df))
            
            logger.info(f"Summary report generated: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Error generating summary report: {str(e)}")
            return None
    
    def _get_leads_for_date(self, date: datetime) -> List[Dict[str, Any]]:
        """Get all leads for a specific date"""
        try:
            # This would typically query HubSpot API for leads created on the specific date
            # For now, return empty list as placeholder
            return []
            
        except Exception as e:
            logger.error(f"Error getting leads for date: {str(e)}")
            return []
    
    def _send_report_to_admin(self, report_paths: List[str], lead_data: Dict[str, Any]):
        """Send report to admin via email"""
        try:
            admin_email = os.getenv('ADMIN_EMAIL')
            
            if not admin_email:
                logger.warning("ADMIN_EMAIL not configured, skipping email send")
                return
            
            # In production, this would send the reports via email
            # For now, just log the action
            logger.info(f"Reports ready to send to admin: {admin_email}")
            logger.info(f"Report files: {report_paths}")
            logger.info(f"Lead data: {lead_data}")
            
        except Exception as e:
            logger.error(f"Error sending report to admin: {str(e)}") 