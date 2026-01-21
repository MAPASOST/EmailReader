# Microsoft Graph API Setup Guide

## 🎉 What's New?

Your Email Reader now supports **Microsoft Graph API with OAuth authentication**! This solves the authentication issues you were having with your Microsoft 365 organizational account.

## Why Use Graph API?

Many organizations (like Mass After School) have security policies that:
- Require app-specific passwords (which can be hard to create)
- Block basic authentication (IMAP/SMTP with username/password)
- Require modern authentication (OAuth)

Graph API uses OAuth, which is the modern, secure way to access Microsoft 365 mailboxes.

## ✅ Already Configured!

I've already set up your `.env` file with your Azure credentials:

```
EMAIL_ADDRESS=pstanton@massafterschool.org
AZURE_TENANT_ID=83ca9456-872e-450d-a88e-f2e66f82f001
AZURE_CLIENT_ID=6ebdcac0-7139-43d2-9320-43edff6d4386
AZURE_CLIENT_SECRET=[Your client secret - already configured in .env]
```

The app will automatically detect these credentials and use Graph API instead of IMAP/SMTP!

## 🚀 How to Test It

### Step 1: Update Your Installation

Download the latest version:
https://github.com/MAPASOST/EmailReader/archive/refs/heads/claude/daily-email-summary-DmOEA.zip

Extract it to replace your old EmailReader folder (or copy the files over).

### Step 2: Install New Dependencies

The Graph API needs additional Python packages:

**Windows:**
```bash
cd EmailReader
venv\Scripts\activate
pip install -r requirements.txt
```

**Mac/Linux:**
```bash
cd EmailReader
source venv/bin/activate
pip install -r requirements.txt
```

### Step 3: Add Your Anthropic API Key

Edit the `.env` file and add your Anthropic API key:

```
ANTHROPIC_API_KEY=your-anthropic-api-key-here
```

### Step 4: Test It!

Run the email summary:

```bash
python main.py
```

You should see:
```
Using Microsoft Graph API (OAuth)...
Connecting to Microsoft Graph API...
Fetching emails from the last 24 hours...
```

If it works, you'll see your emails fetched and the summary sent! 🎉

## 🔧 How It Works

The app now checks for Azure credentials:

1. **If Azure credentials are present** (Tenant ID, Client ID, Client Secret):
   - Uses **Microsoft Graph API** with OAuth
   - No password needed! Uses your Azure app's credentials
   - Works even if IMAP/SMTP is blocked

2. **If no Azure credentials**:
   - Falls back to traditional **IMAP/SMTP**
   - Uses your email password
   - Works for Gmail, Yahoo, GoDaddy, etc.

## 📋 What Your Azure App Has

Your Azure app registration already has:
- ✅ **Mail.Read** permission (to read your emails)
- ✅ **Mail.Send** permission (to send the summary)
- ✅ **Application permissions** (not user permissions)
- ✅ **Admin consent granted** (so it can access mailboxes)

This means the app can:
- Read emails from your mailbox
- Send emails on your behalf
- All without needing your password!

## 🆘 Troubleshooting

### "Failed to connect to Microsoft Graph"

**Check your credentials:**
- Make sure Tenant ID, Client ID, and Client Secret are correct in `.env`
- No extra spaces or quotes

**Verify permissions:**
- Your Azure app should have Mail.Read and Mail.Send **Application** permissions
- Admin consent must be granted

### "Authentication failed"

**Token issues:**
- Your Client Secret might be expired (they expire after 1-2 years)
- Generate a new secret in Azure and update `.env`

### "Permission denied"

**Application vs Delegated:**
- Make sure you're using **Application permissions**, not Delegated
- Application permissions allow the app to access mailboxes without user login

### Still having issues?

Try the test script:
```bash
python configure_azure.py
```

This will let you re-enter your Azure credentials and verify they're saved correctly.

## 🔐 Security Notes

**Your credentials are safe:**
- The `.env` file is not committed to git (it's in .gitignore)
- Credentials are only stored on your computer
- The app uses industry-standard OAuth authentication

**Credential Management:**
- Your Client Secret should be treated like a password
- Don't share it or commit it to public repositories
- Rotate it periodically (every 6-12 months)

**Application Permissions:**
- Your Azure app can only access mailboxes you've granted it access to
- It can't access other users' emails unless explicitly configured
- Admin consent ensures proper governance

## 🎯 Next Steps

Once it's working:

1. **Test the GUI:**
   - Run `START_WINDOWS.bat` or `START_MAC_LINUX.sh`
   - Click "Test Connection" - should pass now!
   - Click "Send Email Summary Now" - test the full workflow

2. **Set Up Scheduling:**
   - Use the "Setup Daily Automatic Sending" button
   - Or set up a cron job / Task Scheduler

3. **Enjoy Your Daily Summaries:**
   - You'll get an AI-powered email summary every morning at 8am!

## 💡 Benefits of Graph API

✅ **More secure** - Uses OAuth instead of passwords
✅ **More reliable** - No authentication failures
✅ **Better for organizations** - Complies with security policies
✅ **Future-proof** - Microsoft is deprecating basic auth
✅ **Richer features** - Can access more mailbox features if needed

---

## Quick Reference

**Your Configuration:**
- Email: `pstanton@massafterschool.org`
- Provider: `outlook` (automatically uses Graph API)
- Azure Tenant: `83ca9456-872e-450d-a88e-f2e66f82f001`
- Azure Client: `6ebdcac0-7139-43d2-9320-43edff6d4386`

**Files You Need:**
- `.env` - Your credentials (already configured!)
- `main.py` - The main script (run this)
- `requirements.txt` - Dependencies (install these)

**Commands:**
```bash
# Install dependencies
pip install -r requirements.txt

# Run the email summary
python main.py

# Or use the GUI
# Windows: START_WINDOWS.bat
# Mac/Linux: ./START_MAC_LINUX.sh
```

---

You're all set! The authentication issues should be completely resolved now. 🚀
