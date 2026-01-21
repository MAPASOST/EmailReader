"""
Main script for email reader and summarizer.
"""
import os
from dotenv import load_dotenv
from email_reader import EmailReader
from email_summarizer import EmailSummarizer
from email_sender import EmailSender
from graph_email_reader import GraphEmailReader
from graph_email_sender import GraphEmailSender
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
        'email_provider': os.getenv('EMAIL_PROVIDER', 'outlook'),
        'imap_server': os.getenv('IMAP_SERVER', 'outlook.office365.com'),
        'imap_port': int(os.getenv('IMAP_PORT', '993')),
        'smtp_server': os.getenv('SMTP_SERVER', 'smtp.office365.com'),
        'smtp_port': int(os.getenv('SMTP_PORT', '587')),
        'anthropic_api_key': os.getenv('ANTHROPIC_API_KEY'),
        # Azure/Graph API credentials (optional)
        'azure_tenant_id': os.getenv('AZURE_TENANT_ID'),
        'azure_client_id': os.getenv('AZURE_CLIENT_ID'),
        'azure_client_secret': os.getenv('AZURE_CLIENT_SECRET'),
    }

    # Validate required fields
    required_fields = ['email_address', 'anthropic_api_key']
    missing_fields = [field for field in required_fields if not config[field]]

    if missing_fields:
        raise ValueError(f"Missing required configuration: {', '.join(missing_fields)}")

    return config


def use_graph_api(config):
    """
    Determine if we should use Graph API instead of IMAP/SMTP.

    Returns:
        True if Azure credentials are available and provider is outlook
    """
    return (config.get('email_provider') == 'outlook' and
            config.get('azure_tenant_id') and
            config.get('azure_client_id') and
            config.get('azure_client_secret'))


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

        # Determine which method to use
        if use_graph_api(config):
            print("Using Microsoft Graph API (OAuth)...")

            # Initialize Graph email reader
            print(f"Connecting to Microsoft Graph API...")
            reader = GraphEmailReader(
                tenant_id=config['azure_tenant_id'],
                client_id=config['azure_client_id'],
                client_secret=config['azure_client_secret'],
                user_email=config['email_address']
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

            # Send summary email via Graph API
            print(f"Sending summary email to {config['email_address']}...")
            sender = GraphEmailSender(
                tenant_id=config['azure_tenant_id'],
                client_id=config['azure_client_id'],
                client_secret=config['azure_client_secret'],
                user_email=config['email_address']
            )

            success = sender.send_summary(
                to_address=config['email_address'],
                summary_html=summary
            )

        else:
            print("Using IMAP/SMTP...")

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

            # Send summary email via SMTP
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
