"""
Email sender module for sending summary emails via SMTP.
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime


class EmailSender:
    def __init__(self, email_address: str, password: str, smtp_server: str, smtp_port: int = 587):
        """
        Initialize the email sender.

        Args:
            email_address: Email address for SMTP login
            password: Password or app-specific password
            smtp_server: SMTP server address
            smtp_port: SMTP server port (default: 587 for TLS)
        """
        self.email_address = email_address
        self.password = password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port

    def send_summary(self, to_address: str, summary_html: str) -> bool:
        """
        Send the email summary.

        Args:
            to_address: Recipient email address
            summary_html: HTML content of the summary

        Returns:
            True if email sent successfully, False otherwise
        """
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = self.email_address
            msg['To'] = to_address
            msg['Subject'] = f"Daily Email Summary - {datetime.now().strftime('%B %d, %Y')}"

            # Attach HTML content
            html_part = MIMEText(summary_html, 'html')
            msg.attach(html_part)

            # Connect to SMTP server and send
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # Upgrade to secure connection
                server.login(self.email_address, self.password)
                server.send_message(msg)

            print(f"Summary email sent successfully to {to_address}")
            return True

        except Exception as e:
            print(f"Failed to send email: {e}")
            return False
