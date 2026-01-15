# EmailReader

An automated email summary tool that reads your emails every 24 hours and sends you an AI-powered summary at 8am daily.

---

## 🎯 NEW! Simple Interface for Everyone

**Not a programmer?** No problem! We now have a simple point-and-click interface!

### For Beginners (No Coding Required):
1. Read the **[BEGINNER_GUIDE.md](BEGINNER_GUIDE.md)** - Simple instructions in plain English
2. **Windows**: Run `INSTALL_WINDOWS.bat` then `START_WINDOWS.bat`
3. **Mac/Linux**: Run `./INSTALL_MAC_LINUX.sh` then `./START_MAC_LINUX.sh`

You'll get a friendly window where you can:
- Select your email provider (Gmail, Outlook, Yahoo, iCloud)
- Enter your email and credentials with a simple form
- Test if everything works with one click
- Send summaries instantly with one button
- Set up automatic daily sending with easy instructions

### For Developers:
Continue reading below for the technical documentation and command-line usage.

---

## Features

- **Multi-Provider Support**: Works with Gmail, Outlook/Office 365, Yahoo Mail, iCloud, and GoDaddy
- **AI-Powered Summaries**: Uses Claude AI to create intelligent, organized summaries
- **Automatic Scheduling**: Sends a summary email every morning at 8am (configurable)
- **Smart Organization**: Highlights important emails and groups similar ones together
- **Action Items**: Identifies emails requiring urgent attention
- **Privacy First**: Runs locally on your machine with full privacy control
- **Easy Setup**: Beginner-friendly GUI with one-click installers

## Prerequisites

- Python 3.8 or higher
- Email account with one of these providers:
  - Gmail / Google Workspace
  - Outlook / Office 365 / Hotmail
  - Yahoo Mail
  - iCloud Mail
  - GoDaddy Email Hosting
- Anthropic API key (for Claude AI - free credits available)

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd EmailReader
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and fill in your credentials:

```env
# Your Outlook/Office 365 email
EMAIL_ADDRESS=your-email@outlook.com
EMAIL_PASSWORD=your-password-here

# IMAP Settings (default values work for Outlook)
IMAP_SERVER=outlook.office365.com
IMAP_PORT=993

# SMTP Settings (default values work for Outlook)
SMTP_SERVER=smtp.office365.com
SMTP_PORT=587

# Claude AI API Key (get from https://console.anthropic.com/)
ANTHROPIC_API_KEY=your-anthropic-api-key-here

# Summary time (24-hour format)
SUMMARY_TIME=08:00

# Optional: Timezone (not currently used but available for future features)
TIMEZONE=America/New_York
```

### Getting Your Anthropic API Key

1. Go to https://console.anthropic.com/
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy it to your `.env` file

### Email Account Security

For Outlook/Office 365:
- If you have 2FA enabled, you may need to use an app-specific password
- Go to your Microsoft account security settings to generate one

## Usage

### Option 1: Run Manually (Test)

Test the email summary immediately:

```bash
python main.py
```

This will:
1. Connect to your email account
2. Fetch emails from the last 24 hours
3. Generate an AI summary
4. Send the summary to your email address

### Option 2: Run with Built-in Scheduler

Run the scheduler that will execute the summary at 8am daily:

```bash
python scheduler.py
```

The scheduler will:
- Run continuously in the background
- Execute the email summary every day at the configured time (default: 8am)
- Display logs for each execution

To stop the scheduler, press `Ctrl+C`.

### Option 3: Use System Scheduler (Recommended for Production)

For a more robust solution, use your system's task scheduler:

#### Linux/Mac (cron)

1. Edit your crontab:
```bash
crontab -e
```

2. Add this line (adjust the path to your project):
```bash
0 8 * * * cd /path/to/EmailReader && /path/to/EmailReader/venv/bin/python main.py >> /path/to/EmailReader/logs.txt 2>&1
```

This runs the script every day at 8:00 AM.

#### Windows (Task Scheduler)

1. Open Task Scheduler
2. Create a new task
3. Set trigger: Daily at 8:00 AM
4. Set action: Start a program
   - Program: `C:\path\to\EmailReader\venv\Scripts\python.exe`
   - Arguments: `main.py`
   - Start in: `C:\path\to\EmailReader`

## Project Structure

```
EmailReader/
├── main.py              # Main orchestration script
├── email_reader.py      # IMAP email reading functionality
├── email_summarizer.py  # Claude AI summarization
├── email_sender.py      # SMTP email sending
├── scheduler.py         # Built-in scheduler (optional)
├── requirements.txt     # Python dependencies
├── .env.example         # Example configuration file
├── .env                 # Your actual configuration (not in git)
├── .gitignore          # Git ignore file
└── README.md           # This file
```

## How It Works

1. **Email Reading**: Connects to your Outlook account via IMAP and fetches all emails from the last 24 hours
2. **AI Summarization**: Sends email content to Claude AI which creates an organized, intelligent summary that:
   - Highlights the most important emails
   - Groups similar emails together
   - Identifies urgent items requiring attention
   - Provides brief summaries of each email's content
3. **Email Delivery**: Sends the formatted HTML summary back to your email address via SMTP

## Troubleshooting

### Authentication Errors

- Make sure you're using the correct email and password
- For Outlook with 2FA, generate an app-specific password
- Check that IMAP/SMTP access is enabled in your email account settings

### No Emails Found

- The script only fetches emails from the last 24 hours
- Check that you actually received emails in that timeframe
- Verify the IMAP connection is working

### Claude API Errors

- Verify your API key is correct
- Check your API usage limits at https://console.anthropic.com/
- Ensure you have credits available in your Anthropic account

### Scheduler Not Running

- Make sure the scheduler.py process is running
- Check that the time format is correct (HH:MM in 24-hour format)
- Verify your system time is correct

## Security Notes

- Never commit your `.env` file to version control
- Store your API keys and passwords securely
- Consider using environment variables or a secrets manager for production
- The `.gitignore` file is configured to exclude `.env` automatically

## Customization

### Change Summary Time

Edit the `SUMMARY_TIME` in your `.env` file:
```env
SUMMARY_TIME=09:30  # 9:30 AM
```

### Customize Summary Format

Edit the prompt in `email_summarizer.py` to change how Claude summarizes your emails.

### Change Email Lookback Period

In `email_reader.py`, modify the `fetch_emails_last_24h()` method to fetch from a different time period.

## License

MIT License - feel free to use and modify as needed.

## Support

For issues or questions, please create an issue in the repository.