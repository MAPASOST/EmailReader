"""
GoDaddy Email Connection Test Script

This script tests your GoDaddy email connection and shows detailed error messages.
Run this to diagnose connection issues.
"""

import imaplib
import smtplib
import getpass


def test_godaddy_imap(email, password):
    """Test IMAP connection to GoDaddy."""
    print("\n" + "="*60)
    print("Testing IMAP Connection (Incoming Mail)")
    print("="*60)

    servers_to_try = [
        ("imap.secureserver.net", 993),
        ("imap.secureserver.net", 143),
    ]

    for server, port in servers_to_try:
        print(f"\nTrying {server}:{port}...")
        try:
            if port == 993:
                # Try SSL
                mail = imaplib.IMAP4_SSL(server, port)
            else:
                # Try without SSL
                mail = imaplib.IMAP4(server, port)
                mail.starttls()

            print("  ✓ Connected to server")

            # Try to login
            mail.login(email, password)
            print("  ✓ Login successful!")

            # List mailboxes
            status, mailboxes = mail.list()
            if status == 'OK':
                print(f"  ✓ Found {len(mailboxes)} mailboxes")

            # Select inbox
            status, messages = mail.select('INBOX')
            if status == 'OK':
                print(f"  ✓ Inbox has {messages[0].decode()} messages")

            mail.close()
            mail.logout()

            print(f"\n✅ SUCCESS! IMAP is working on {server}:{port}")
            return True

        except imaplib.IMAP4.error as e:
            print(f"  ✗ IMAP Error: {e}")
        except Exception as e:
            print(f"  ✗ Connection Error: {e}")

    print("\n❌ IMAP connection failed on all servers")
    return False


def test_godaddy_smtp(email, password):
    """Test SMTP connection to GoDaddy."""
    print("\n" + "="*60)
    print("Testing SMTP Connection (Outgoing Mail)")
    print("="*60)

    servers_to_try = [
        ("smtpout.secureserver.net", 465, True),   # SSL
        ("smtpout.secureserver.net", 587, False),  # TLS
        ("smtpout.secureserver.net", 80, False),   # Alternative
    ]

    for server, port, use_ssl in servers_to_try:
        print(f"\nTrying {server}:{port} ({'SSL' if use_ssl else 'TLS'})...")
        try:
            if use_ssl:
                # SSL connection
                smtp = smtplib.SMTP_SSL(server, port, timeout=10)
            else:
                # Regular connection with STARTTLS
                smtp = smtplib.SMTP(server, port, timeout=10)
                smtp.ehlo()
                smtp.starttls()
                smtp.ehlo()

            print("  ✓ Connected to server")

            # Try to login
            smtp.login(email, password)
            print("  ✓ Login successful!")

            smtp.quit()

            print(f"\n✅ SUCCESS! SMTP is working on {server}:{port}")
            return True

        except smtplib.SMTPAuthenticationError as e:
            print(f"  ✗ Authentication Error: {e}")
        except Exception as e:
            print(f"  ✗ Connection Error: {e}")

    print("\n❌ SMTP connection failed on all servers")
    return False


def main():
    print("="*60)
    print("GoDaddy Email Connection Test")
    print("="*60)
    print("\nThis script will test your GoDaddy email connection.")
    print("It will try different server configurations to find what works.\n")

    # Get credentials
    email = input("Enter your email address (e.g., pstanton@massafterschool.org): ").strip()
    password = getpass.getpass("Enter your email password: ")

    if not email or not password:
        print("\n❌ Error: Email and password are required!")
        return

    print(f"\nTesting connection for: {email}")

    # Test IMAP
    imap_success = test_godaddy_imap(email, password)

    # Test SMTP
    smtp_success = test_godaddy_smtp(email, password)

    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    print(f"IMAP (Incoming): {'✅ Working' if imap_success else '❌ Failed'}")
    print(f"SMTP (Outgoing): {'✅ Working' if smtp_success else '❌ Failed'}")

    if not imap_success or not smtp_success:
        print("\n" + "="*60)
        print("Troubleshooting Tips")
        print("="*60)
        print("\n1. Check your email and password are correct")
        print("   - Try logging into GoDaddy Workspace Webmail")
        print("   - Use the exact same password")

        print("\n2. Make sure IMAP/SMTP is enabled:")
        print("   - Log into workspace.godaddy.com")
        print("   - Go to Settings > Forwarding and POP/IMAP")
        print("   - Enable IMAP access")

        print("\n3. Check if you're using the right email type:")
        print("   - GoDaddy Workspace Email (formerly Office 365)")
        print("   - GoDaddy Email & Office (different servers)")
        print("   - GoDaddy cPanel Email (different servers)")

        print("\n4. Try these alternative servers in the app:")
        print("   For some GoDaddy accounts, try:")
        print("   - IMAP: imap.secureserver.net:143 (without SSL)")
        print("   - SMTP: smtpout.secureserver.net:587 (TLS)")

        print("\n5. Contact GoDaddy Support:")
        print("   - They can verify your account type")
        print("   - Ask for the correct IMAP/SMTP server settings")
        print("   - Make sure email forwarding isn't interfering")
    else:
        print("\n✅ All tests passed! Your email should work in the app.")
        print("\nIf it still doesn't work in the Email Reader app:")
        print("1. Make sure you selected 'godaddy' from the provider dropdown")
        print("2. Use the exact same email and password you just tested")
        print("3. Click 'Test Connection' in the app")

    print("\n" + "="*60)
    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()
