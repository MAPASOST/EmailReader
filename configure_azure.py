"""
Quick configuration script to set up Azure credentials for Microsoft Graph API.
"""
from dotenv import set_key
from pathlib import Path


def configure_azure():
    """Configure Azure credentials in .env file."""
    print("="*60)
    print("Azure/Microsoft 365 OAuth Configuration")
    print("="*60)
    print("\nThis will configure Email Reader to use Microsoft Graph API")
    print("instead of IMAP/SMTP for Microsoft 365 accounts.")
    print("\nYou'll need:")
    print("1. Azure Tenant ID")
    print("2. Azure App Client ID")
    print("3. Azure App Client Secret")
    print("\nThese should be from an Azure AD app registration with")
    print("Mail.Read and Mail.Send application permissions.\n")

    # Get Azure credentials
    tenant_id = input("Enter your Azure Tenant ID: ").strip()
    client_id = input("Enter your Azure Client ID: ").strip()
    client_secret = input("Enter your Azure Client Secret: ").strip()
    email = input("Enter your Microsoft 365 email address: ").strip()

    if not all([tenant_id, client_id, client_secret, email]):
        print("\n❌ Error: All fields are required!")
        return

    # Create .env if it doesn't exist
    env_file = Path('.env')
    if not env_file.exists():
        print("\nCreating .env file from template...")
        with open('.env.example', 'r') as f:
            content = f.read()
        with open('.env', 'w') as f:
            f.write(content)

    # Update .env file
    print("\nUpdating .env file...")
    set_key('.env', 'EMAIL_ADDRESS', email)
    set_key('.env', 'EMAIL_PROVIDER', 'outlook')
    set_key('.env', 'AZURE_TENANT_ID', tenant_id)
    set_key('.env', 'AZURE_CLIENT_ID', client_id)
    set_key('.env', 'AZURE_CLIENT_SECRET', client_secret)

    print("\n✅ Configuration saved!")
    print("\nNext steps:")
    print("1. Make sure you have your Anthropic API key configured")
    print("2. Run: python main.py")
    print("\nThe app will automatically use Microsoft Graph API")
    print("instead of IMAP/SMTP for your Microsoft 365 account.")
    print("\n" + "="*60)


if __name__ == "__main__":
    configure_azure()
