"""
Quick test for pstanton@massafterschool.org
"""
import imaplib
import smtplib

email = "pstanton@massafterschool.org"
password = "Tremont2beacon."

print("="*60)
print("Testing GoDaddy Email Connection")
print("="*60)
print(f"\nEmail: {email}")
print()

# Test 1: IMAP with SSL on port 993
print("Test 1: IMAP (imap.secureserver.net:993 with SSL)")
print("-" * 60)
try:
    mail = imaplib.IMAP4_SSL("imap.secureserver.net", 993, timeout=15)
    print("  ✓ Connected to server")

    mail.login(email, password)
    print("  ✓ Login successful!")

    status, mailboxes = mail.list()
    print(f"  ✓ Found {len(mailboxes)} mailboxes")

    status, messages = mail.select('INBOX')
    print(f"  ✓ Inbox has {messages[0].decode()} messages")

    mail.close()
    mail.logout()
    print("\n✅ IMAP TEST PASSED!")
    imap_works = True
except Exception as e:
    print(f"  ✗ FAILED: {e}")
    imap_works = False

print()

# Test 2: SMTP with SSL on port 465
print("Test 2: SMTP (smtpout.secureserver.net:465 with SSL)")
print("-" * 60)
try:
    smtp = smtplib.SMTP_SSL("smtpout.secureserver.net", 465, timeout=15)
    print("  ✓ Connected to server")

    smtp.login(email, password)
    print("  ✓ Login successful!")

    smtp.quit()
    print("\n✅ SMTP TEST PASSED!")
    smtp_works = True
except Exception as e:
    print(f"  ✗ FAILED: {e}")
    smtp_works = False

print()

# Test 3: Alternative SMTP with TLS on port 587
if not smtp_works:
    print("Test 3: SMTP Alternative (smtpout.secureserver.net:587 with TLS)")
    print("-" * 60)
    try:
        smtp = smtplib.SMTP("smtpout.secureserver.net", 587, timeout=15)
        print("  ✓ Connected to server")

        smtp.starttls()
        print("  ✓ Started TLS")

        smtp.login(email, password)
        print("  ✓ Login successful!")

        smtp.quit()
        print("\n✅ SMTP TEST PASSED!")
        smtp_works = True
    except Exception as e:
        print(f"  ✗ FAILED: {e}")
        smtp_works = False
    print()

# Summary
print("="*60)
print("FINAL RESULTS")
print("="*60)
print(f"IMAP (Reading Email): {'✅ WORKING' if imap_works else '❌ FAILED'}")
print(f"SMTP (Sending Email): {'✅ WORKING' if smtp_works else '❌ FAILED'}")
print()

if imap_works and smtp_works:
    print("🎉 SUCCESS! Your email is working correctly!")
    print("\nYour GoDaddy settings are:")
    print("  IMAP Server: imap.secureserver.net")
    print("  IMAP Port: 993")
    print("  SMTP Server: smtpout.secureserver.net")
    print("  SMTP Port: 465")
else:
    print("❌ Some tests failed. See error messages above.")
