"""
Microsoft Graph API email sender module for Microsoft 365 accounts.
"""
from datetime import datetime
from azure.identity import ClientSecretCredential
from msgraph import GraphServiceClient
from msgraph.generated.models.message import Message
from msgraph.generated.models.item_body import ItemBody
from msgraph.generated.models.body_type import BodyType
from msgraph.generated.models.recipient import Recipient
from msgraph.generated.models.email_address import EmailAddress


class GraphEmailSender:
    def __init__(self, tenant_id: str, client_id: str, client_secret: str, user_email: str):
        """
        Initialize the Graph API email sender.

        Args:
            tenant_id: Azure AD tenant ID
            client_id: Azure app client ID
            client_secret: Azure app client secret
            user_email: Email address of the user sending the email
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

    def send_summary(self, to_address: str, summary_html: str) -> bool:
        """
        Send the email summary using Microsoft Graph API.

        Args:
            to_address: Recipient email address
            summary_html: HTML content of the summary

        Returns:
            True if email sent successfully, False otherwise
        """
        if not self.client:
            if not self.connect():
                return False

        try:
            # Create the message
            message = Message()
            message.subject = f"Daily Email Summary - {datetime.now().strftime('%B %d, %Y')}"

            # Set HTML body
            message.body = ItemBody()
            message.body.content_type = BodyType.Html
            message.body.content = summary_html

            # Set recipient
            to_recipient = Recipient()
            to_recipient.email_address = EmailAddress()
            to_recipient.email_address.address = to_address
            message.to_recipients = [to_recipient]

            # Send the message
            self.client.users.by_user_id(self.user_email).send_mail.post(
                body={
                    "message": message,
                    "saveToSentItems": True
                }
            )

            print(f"Summary email sent successfully to {to_address} via Graph API")
            return True

        except Exception as e:
            print(f"Failed to send email via Graph API: {e}")
            return False
