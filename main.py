"""
Main script for email reader and summarizer.
"""
import os
from dotenv import load_dotenv
from email_reader import EmailReader
from email_summarizer import EmailSummarizer
from email_sender import EmailSender
from datetime import datetime


def load_config():
    """
    Load configuration from environment variables.

    Returns:
        Dictionary with configuration values
    """
    load_dotenv()

    config = {
        'email_address': os.getenv('EMAIL_ADDRESS'),
        'email_password': os.getenv('EMAIL_PASSWORD'),
        'imap_server': os.getenv('IMAP_SERVER', 'outlook.office365.com'),
        'imap_port': int(os.getenv('IMAP_PORT', '993')),
        'smtp_server': os.getenv('SMTP_SERVER', 'smtp.office365.com'),
        'smtp_port': int(os.getenv('SMTP_PORT', '587')),
        'anthropic_api_key': os.getenv('ANTHROPIC_API_KEY'),
    }

    # Validate required fields
    required_fields = ['email_address', 'email_password', 'anthropic_api_key']
    missing_fields = [field for field in required_fields if not config[field]]

    if missing_fields:
        raise ValueError(f"Missing required configuration: {', '.join(missing_fields)}")

    return config


def run_email_summary():
    """
    Main function to read emails, create summary, and send it.
    """
    print(f"\n{'='*60}")
    print(f"Email Summary Job Started - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

    try:
        # Load configuration
        print("Loading configuration...")
        config = load_config()

        # Initialize email reader
        print(f"Connecting to IMAP server ({config['imap_server']})...")
        reader = EmailReader(
            email_address=config['email_address'],
            password=config['email_password'],
            imap_server=config['imap_server'],
            imap_port=config['imap_port']
        )

        # Fetch emails from last 24 hours
        print("Fetching emails from the last 24 hours...")
        emails = reader.fetch_emails_last_24h()
        reader.disconnect()

        if not emails:
            print("No emails found in the last 24 hours.")
            return

        # Create AI-powered summary
        print(f"Creating AI-powered summary of {len(emails)} emails...")
        summarizer = EmailSummarizer(api_key=config['anthropic_api_key'])
        summary = summarizer.create_summary(emails)

        # Send summary email
        print(f"Sending summary email to {config['email_address']}...")
        sender = EmailSender(
            email_address=config['email_address'],
            password=config['email_password'],
            smtp_server=config['smtp_server'],
            smtp_port=config['smtp_port']
        )

        success = sender.send_summary(
            to_address=config['email_address'],
            summary_html=summary
        )

        if success:
            print("\n✓ Email summary completed successfully!")
        else:
            print("\n✗ Failed to send summary email")

    except Exception as e:
        print(f"\n✗ Error: {e}")
        raise

    finally:
        print(f"\n{'='*60}")
        print(f"Email Summary Job Ended - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")


if __name__ == "__main__":
    run_email_summary()
