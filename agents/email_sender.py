"""
EmailAgent - Handles sending newsletters via email
"""

import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict
from datetime import datetime
from utils.email_template import NewsletterTemplate


class EmailAgent:
    """Agent responsible for sending newsletter emails."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
    
    async def send_email(self, recipients: List[str], subject: str, summary: str, articles: List[Dict]) -> bool:
        """Send newsletter email to recipients."""
        
        if not self.config.get("email_enabled"):
            print("📧 Email disabled. Set EMAIL_ENABLED=true in .env to enable.")
            return False
        
        # Validate required fields
        required = ["email_user", "email_password"]
        missing = [f for f in required if not self.config.get(f)]
        if missing:
            print(f"❌ Missing email config: {', '.join(missing)}")
            return False
        
        # Clean recipients list
        recipients = [r.strip() for r in recipients if r and r.strip()]
        if not recipients:
            print("⚠️  No recipients specified")
            return False
        
        try:
            print(f"\nSending to {len(recipients)} recipient(s)...")
            
            # Create email
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.config["email_user"]
            msg['To'] = ", ".join(recipients)
            
            # Generate and attach HTML
            html = NewsletterTemplate.generate_html(summary, articles)
            msg.attach(MIMEText(html, 'html', 'utf-8'))
            
            # Send via SMTP
            with smtplib.SMTP(self.config["smtp_server"], self.config["smtp_port"]) as server:
                server.starttls()
                server.login(self.config["email_user"], self.config["email_password"])
                server.send_message(msg)
            
            print(f"✅ Email sent to: {', '.join(recipients)}\n")
            return True
            
        except smtplib.SMTPAuthenticationError:
            print(f"❌ Authentication failed. Check email credentials.")
            return False
        except Exception as e:
            print(f"❌ Failed to send email: {e}")
            return False
    
    async def execute(self, summary: str, articles: List[Dict], recipients: List[str]) -> bool:
        """Execute email sending."""
        subject = f"KeepMePosted - Tech Newsletter {datetime.now().strftime('%B %d, %Y')}"
        return await self.send_email(recipients, subject, summary, articles)
