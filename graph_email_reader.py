"""
Microsoft Graph API email reader module for Microsoft 365 accounts.
"""
from datetime import datetime, timedelta, timezone
from typing import List, Dict
from azure.identity import ClientSecretCredential
from msgraph import GraphServiceClient
from msgraph.generated.users.item.messages.messages_request_builder import MessagesRequestBuilder
from kiota_abstractions.base_request_configuration import RequestConfiguration


class GraphEmailReader:
    def __init__(self, tenant_id: str, client_id: str, client_secret: str, user_email: str):
        """
        Initialize the Graph API email reader.

        Args:
            tenant_id: Azure AD tenant ID
            client_id: Azure app client ID
            client_secret: Azure app client secret
            user_email: Email address of the user whose mailbox to access
        """
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_email = user_email
        self.client = None

    def connect(self) -> bool:
        """
        Connect to Microsoft Graph API.

        Returns:
            True if connection successful, False otherwise
        """
        try:
            credential = ClientSecretCredential(
                tenant_id=self.tenant_id,
                client_id=self.client_id,
                client_secret=self.client_secret
            )

            self.client = GraphServiceClient(credentials=credential)
            return True
        except Exception as e:
            print(f"Failed to connect to Microsoft Graph: {e}")
            return False

    def disconnect(self):
        """Disconnect from Microsoft Graph API."""
        self.client = None

    def fetch_emails_last_24h(self) -> List[Dict]:
        """
        Fetch emails from the last 24 hours using Microsoft Graph API.

        Returns:
            List of email dictionaries with subject, sender, date, and body
        """
        if not self.client:
            if not self.connect():
                return []

        emails = []

        try:
            # Calculate date 24 hours ago in ISO format
            yesterday = datetime.now(timezone.utc) - timedelta(days=1)
            filter_query = f"receivedDateTime ge {yesterday.isoformat()}"

            # Configure the request
            query_params = MessagesRequestBuilder.MessagesRequestBuilderGetQueryParameters(
                filter=filter_query,
                select=['subject', 'from', 'receivedDateTime', 'bodyPreview', 'body'],
                orderby=['receivedDateTime DESC'],
                top=100  # Limit to 100 most recent emails
            )

            request_config = RequestConfiguration(
                query_parameters=query_params
            )

            # Get messages
            messages = self.client.users.by_user_id(self.user_email).messages.get(
                request_configuration=request_config
            )

            if messages and messages.value:
                for msg in messages.value:
                    try:
                        # Extract email details
                        subject = msg.subject or ""
                        sender = msg.from_property.email_address.address if msg.from_property and msg.from_property.email_address else ""
                        sender_name = msg.from_property.email_address.name if msg.from_property and msg.from_property.email_address else ""
                        if sender_name:
                            sender = f"{sender_name} <{sender}>"

                        date = msg.received_date_time or datetime.now(timezone.utc)

                        # Get body preview (first 500 chars)
                        body = msg.body_preview or ""
                        if len(body) > 500:
                            body = body[:500]

                        emails.append({
                            "subject": subject,
                            "sender": sender,
                            "date": date,
                            "body": body
                        })

                    except Exception as e:
                        print(f"Error processing email: {e}")
                        continue

            print(f"Fetched {len(emails)} emails from the last 24 hours via Graph API")

        except Exception as e:
            print(f"Error fetching emails via Graph API: {e}")

        return emails
