"""
EmailAgent - Handles sending newsletters via email
"""

import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict
from datetime import datetime
from utils.email_template import NewsletterTemplate
from utils.retry import retry_on_network_error

logger = logging.getLogger(__name__)


class EmailAgent:
    """Agent responsible for sending newsletter emails."""

    def __init__(self, config: Dict):
        self.config = config

    @retry_on_network_error()
    def _send_smtp(self, msg: MIMEMultipart) -> None:
        """Send email via SMTP with retry logic."""
        with smtplib.SMTP(
            self.config["smtp_server"], self.config["smtp_port"], timeout=30
        ) as server:
            server.starttls()
            server.login(self.config["email_user"], self.config["email_password"])
            server.send_message(msg)

    async def send_email(
        self, recipients: List[str], subject: str, summary: str, articles: List[Dict]
    ) -> bool:
        """Send newsletter email to recipients."""

        if not self.config.get("email_enabled"):
            logger.info("Email sending is disabled")
            print("📧 Email disabled. Set EMAIL_ENABLED=true in .env to enable.")
            return False

        # Validate required fields
        required = ["email_user", "email_password"]
        missing = [f for f in required if not self.config.get(f)]
        if missing:
            logger.error(f"Missing email configuration: {', '.join(missing)}")
            print(f"❌ Missing email config: {', '.join(missing)}")
            return False

        # Clean recipients list
        recipients = [r.strip() for r in recipients if r and r.strip()]
        if not recipients:
            logger.warning("No recipients specified for email")
            print("⚠️  No recipients specified")
            return False

        try:
            logger.info(f"Sending email to {len(recipients)} recipient(s): {subject}")
            print(f"\n📧 Sending to {len(recipients)} recipient(s)...")

            # Create email
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = self.config["email_user"]
            msg["To"] = ", ".join(recipients)

            # Generate and attach HTML
            html = NewsletterTemplate.generate_html(summary, articles)
            msg.attach(MIMEText(html, "html", "utf-8"))

            # Send via SMTP with retry
            self._send_smtp(msg)

            logger.info(f"Email sent successfully to: {', '.join(recipients)}")
            print(f"✅ Email sent to: {', '.join(recipients)}\n")
            return True

        except smtplib.SMTPAuthenticationError as e:
            logger.error(f"SMTP authentication failed: {e}")
            print("❌ Authentication failed. Check email credentials.")
            return False
        except Exception as e:
            logger.error(f"Failed to send email: {e}", exc_info=True)
            print(f"❌ Failed to send email: {e}")
            return False

    async def execute(self, summary: str, articles: List[Dict], recipients: List[str]) -> bool:
        """Execute email sending."""
        subject = f"KeepMePosted - Tech Newsletter {datetime.now().strftime('%B %d, %Y')}"
        return await self.send_email(recipients, subject, summary, articles)
