"""
Email reader module for fetching emails from IMAP server.
"""
import imaplib
import email
from email.header import decode_header
from datetime import datetime, timedelta
from typing import List, Dict
import os


class EmailReader:
    def __init__(self, email_address: str, password: str, imap_server: str, imap_port: int = 993):
        """
        Initialize the email reader.

        Args:
            email_address: Email address for IMAP login
            password: Password or app-specific password
            imap_server: IMAP server address
            imap_port: IMAP server port (default: 993 for SSL)
        """
        self.email_address = email_address
        self.password = password
        self.imap_server = imap_server
        self.imap_port = imap_port
        self.mail = None

    def connect(self) -> bool:
        """
        Connect to the IMAP server.

        Returns:
            True if connection successful, False otherwise
        """
        try:
            self.mail = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            self.mail.login(self.email_address, self.password)
            return True
        except Exception as e:
            print(f"Failed to connect to IMAP server: {e}")
            return False

    def disconnect(self):
        """Disconnect from the IMAP server."""
        if self.mail:
            try:
                self.mail.close()
                self.mail.logout()
            except:
                pass

    def decode_mime_header(self, header: str) -> str:
        """
        Decode MIME encoded email headers.

        Args:
            header: MIME encoded header string

        Returns:
            Decoded string
        """
        if header is None:
            return ""

        decoded_parts = decode_header(header)
        decoded_string = ""

        for part, encoding in decoded_parts:
            if isinstance(part, bytes):
                decoded_string += part.decode(encoding or 'utf-8', errors='ignore')
            else:
                decoded_string += part

        return decoded_string

    def get_email_body(self, msg) -> str:
        """
        Extract email body from message.

        Args:
            msg: Email message object

        Returns:
            Email body as string
        """
        body = ""

        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))

                if content_type == "text/plain" and "attachment" not in content_disposition:
                    try:
                        body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                        break
                    except:
                        pass
        else:
            try:
                body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
            except:
                pass

        return body

    def fetch_emails_last_24h(self, mailbox: str = "INBOX") -> List[Dict]:
        """
        Fetch emails from the last 24 hours.

        Args:
            mailbox: Mailbox to fetch from (default: INBOX)

        Returns:
            List of email dictionaries with subject, sender, date, and body
        """
        if not self.mail:
            if not self.connect():
                return []

        emails = []

        try:
            # Select the mailbox
            self.mail.select(mailbox)

            # Calculate date 24 hours ago
            yesterday = (datetime.now() - timedelta(days=1)).strftime("%d-%b-%Y")

            # Search for emails from the last 24 hours
            status, messages = self.mail.search(None, f'(SINCE {yesterday})')

            if status != "OK":
                print("Failed to search emails")
                return []

            email_ids = messages[0].split()

            # Fetch each email
            for email_id in email_ids:
                try:
                    status, msg_data = self.mail.fetch(email_id, "(RFC822)")

                    if status != "OK":
                        continue

                    # Parse the email
                    msg = email.message_from_bytes(msg_data[0][1])

                    # Extract email details
                    subject = self.decode_mime_header(msg.get("Subject", ""))
                    sender = self.decode_mime_header(msg.get("From", ""))
                    date_str = msg.get("Date", "")
                    body = self.get_email_body(msg)

                    # Parse date
                    try:
                        date = email.utils.parsedate_to_datetime(date_str)
                    except:
                        date = datetime.now()

                    emails.append({
                        "subject": subject,
                        "sender": sender,
                        "date": date,
                        "body": body[:500]  # Limit body to first 500 chars for summary
                    })

                except Exception as e:
                    print(f"Error processing email {email_id}: {e}")
                    continue

            print(f"Fetched {len(emails)} emails from the last 24 hours")

        except Exception as e:
            print(f"Error fetching emails: {e}")

        return emails
