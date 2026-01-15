# 📧 Email Reader - Beginner's Guide

## What does this do?

**Email Reader** automatically reads your emails every morning and sends you a nice summary at 8am (or whatever time you choose).

The summary is created by AI (Claude) and includes:
- The most important emails
- Grouped similar emails (like newsletters together)
- Highlights of what requires your attention
- Short descriptions of what each email is about

You'll receive ONE organized email instead of being overwhelmed by dozens of emails!

---

## 🚀 Quick Start (3 Easy Steps!)

### Step 1: Install Python

**Windows:**
1. Go to https://www.python.org/downloads/
2. Download Python (version 3.8 or newer)
3. Run the installer
4. ⚠️ **IMPORTANT**: Check the box that says "Add Python to PATH"
5. Click "Install Now"

**Mac:**
1. Open Terminal (press Cmd+Space, type "Terminal")
2. Install Homebrew if you don't have it:
   ```
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
3. Install Python:
   ```
   brew install python3
   ```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install python3 python3-venv python3-pip
```

### Step 2: Install Email Reader

**Windows:**
1. Download this folder to your computer
2. Double-click `INSTALL_WINDOWS.bat`
3. Wait for it to finish (it will install everything you need)
4. Press any key when it's done

**Mac/Linux:**
1. Download this folder to your computer
2. Open Terminal
3. Navigate to the folder:
   ```bash
   cd path/to/EmailReader
   ```
4. Run the installer:
   ```bash
   ./INSTALL_MAC_LINUX.sh
   ```

### Step 3: Start the Application

**Windows:**
- Double-click `START_WINDOWS.bat`

**Mac/Linux:**
- Open Terminal, navigate to the folder, and run:
  ```bash
  ./START_MAC_LINUX.sh
  ```

---

## 📝 First Time Setup

When you first open Email Reader, you'll see a setup wizard. You need to enter:

### 1. Your Email Address
Just type your Outlook or Office 365 email address (e.g., `yourname@outlook.com`)

### 2. Your Email Password
- Type your email password
- **If you have 2-factor authentication**, you'll need an "app password" instead:
  1. Go to your Microsoft account security settings
  2. Look for "App passwords"
  3. Create a new app password for "Email Reader"
  4. Use that password instead of your regular password

### 3. Anthropic API Key (for AI)
This is what makes the smart summaries!

**How to get it:**
1. Go to https://console.anthropic.com/
2. Sign up for a free account (they give you free credits!)
3. Go to "API Keys" section
4. Click "Create Key"
5. Copy the key and paste it into Email Reader

**Cost:** Very cheap! Usually costs less than $0.10 per day (about $3/month).

### 4. What time do you want the summary?
- Type the time in 24-hour format
- Examples:
  - `08:00` = 8:00 AM
  - `09:30` = 9:30 AM
  - `13:00` = 1:00 PM
  - `17:30` = 5:30 PM

---

## 🎯 Using Email Reader

After setup, you'll see the main screen with these buttons:

### ⚙️ Setup / Change Settings
Click this to change your email, password, API key, or summary time.

### 🧪 Test Connection
Click this to make sure everything is working correctly. It will:
- Test your email login
- Test your AI API key
- Tell you if there are any problems

**Always test after setting up!**

### ▶️ Send Email Summary Now
Click this to get your email summary RIGHT NOW (doesn't wait until 8am).

This is great for:
- Testing if everything works
- Getting a summary whenever you want
- Checking what your daily summary will look like

### 🕐 Setup Daily Automatic Sending
Click this to see instructions for making it run automatically every day.

**Three options:**
1. **Easy Way (Recommended)** - Keep a small window open on your computer
2. **Windows Advanced** - Use Windows Task Scheduler (runs in background)
3. **Mac/Linux Advanced** - Use cron (runs in background)

---

## ❓ Common Questions

### Q: Is this safe? Won't someone see my passwords?
**A:** All your passwords and API keys stay on YOUR computer. They're stored in a file called `.env` that only you can see. Nothing is sent anywhere except:
- Your email credentials go to Microsoft (to read your emails)
- Your email content goes to Anthropic (to create the summary)

Both are legitimate, secure companies.

### Q: How much does this cost?
**A:**
- The software: **FREE**
- Python: **FREE**
- Anthropic API: **Very cheap** - usually $0.05-$0.10 per day (about $2-3 per month)

They give you $5 free credit when you sign up, which lasts about 2 months!

### Q: Does my computer need to be on at 8am?
**A:**
- **If using the "Easy Way"**: Yes, your computer must be on and the scheduler program must be running
- **If using Task Scheduler/cron**: Yes, but your computer can be sleeping (not fully shut down)

### Q: Can I change what time it sends?
**A:** Yes! Just click "Setup / Change Settings" and change the time.

### Q: What if I get an error?
**A:**
1. First, click "Test Connection" to see what's wrong
2. Common fixes:
   - **Email error**: Check your email and password are correct
   - **API error**: Check your Anthropic API key is correct
   - **No emails found**: The program looks at the last 24 hours - if you haven't received emails in that time, you'll see this message

### Q: Can I use Gmail instead of Outlook?
**A:** The current version is set up for Outlook/Office 365. Gmail requires different settings. If you need Gmail support, ask in the issues section!

### Q: Will this work on my old computer?
**A:** As long as you can install Python and have an internet connection, yes!

---

## 🆘 Troubleshooting

### "Python is not recognized..."
- Windows: You need to reinstall Python and check "Add Python to PATH"
- Mac/Linux: Use `python3` instead of `python`

### "Failed to install packages"
- Make sure you have an internet connection
- Try running the installer again

### "Could not connect to email"
- Check your email address and password
- If you have 2-factor authentication, use an app password
- Make sure you're using Outlook/Office 365 (not Gmail)

### "API key is invalid"
- Go to https://console.anthropic.com/
- Make sure you copied the entire API key
- Check that your account has credits remaining

### The window closes immediately
- This is normal on Mac/Linux
- The application should still be running
- Check for a window called "Email Reader"

---

## 🎉 You're All Set!

Once everything is working:
1. Click "Send Email Summary Now" to see your first summary
2. Set up automatic daily sending using the instructions
3. Enjoy getting one organized summary instead of email overload!

---

## 💡 Tips

- **Test it first!** Click "Send Email Summary Now" before setting up automatic sending
- **Check your spam folder** the first time - some email providers might filter the summary email
- **Adjust the time** if 8am doesn't work for you - pick whenever you usually check email
- **Keep your API key private** - don't share it with anyone

---

## Need More Help?

If you're stuck, you can:
1. Read the technical README.md file
2. Create an issue on GitHub
3. Ask a tech-savvy friend to help with the setup

Remember: Setup is the hardest part! Once it's working, you don't have to touch it again. 🎯
