# 🔄 How to Update Email Reader

If you already have Email Reader installed and want to get the latest version with new features (like GoDaddy support!), follow these simple steps:

---

## Option 1: Quick Update (Recommended for Beginners)

This is the easiest way - just download the new version and replace the old files.

### Step 1: Download the Latest Version
Go to: https://github.com/MAPASOST/EmailReader/archive/refs/heads/claude/daily-email-summary-DmOEA.zip

Click to download the ZIP file.

### Step 2: Find Your Old Installation
Look for the folder where you installed Email Reader (probably on your Desktop or in Documents).

### Step 3: Backup Your Settings (Important!)
Before doing anything, make a copy of your `.env` file:
1. Open your Email Reader folder
2. Find the file named `.env` (it might be hidden)
3. Copy it to your Desktop or somewhere safe
4. This file has all your passwords and settings!

**Windows - Show hidden files:**
- Open the folder
- Click "View" at the top
- Check "Hidden items"

**Mac - Show hidden files:**
- In Finder, press `Command + Shift + .` (period)

### Step 4: Extract the New Version
1. Extract the downloaded ZIP file
2. You'll see a new folder with all the updated files

### Step 5: Replace the Files
**Option A - Safe Method (Recommended):**
1. Rename your old Email Reader folder to "EmailReader_OLD"
2. Move the new folder to the same location
3. Rename it to "EmailReader"
4. Copy your `.env` file from the backup into this new folder

**Option B - Replace Method:**
1. Open both folders (old and new) side by side
2. Copy ALL files from the new folder
3. Paste them into your old folder
4. When asked "Replace files?", click "Yes to All"
5. Your `.env` file will be safe (we're not replacing it)

### Step 6: Test It
1. Double-click the START file (START_WINDOWS.bat or START_MAC_LINUX.sh)
2. The app should open with all your settings still saved
3. You should now see "GoDaddy" as an option in the provider dropdown!

---

## Option 2: Update Using Git (For Advanced Users)

If you used git to clone the repository:

```bash
cd /path/to/EmailReader
git pull origin claude/daily-email-summary-DmOEA
```

Your `.env` file will automatically be preserved (it's in .gitignore).

---

## Option 3: Start Fresh

If you want to start completely fresh:

1. Delete your old Email Reader folder
2. Download and extract the new version
3. Run the INSTALL file again
4. Go through setup again with your email and API key

This is the cleanest option but requires re-entering your settings.

---

## ✅ How to Know If Update Worked

After updating, open the app and click "Setup / Change Settings". You should see:
- **GoDaddy** in the email provider dropdown
- All your old settings still there (email address, API key, etc.)

If you see GoDaddy in the list, the update worked! 🎉

---

## ⚠️ Common Issues

### "My settings are gone!"
- Did you backup your `.env` file?
- Copy it back into the Email Reader folder
- Restart the app

### "The app won't start"
- Try running the INSTALL file again
- It will reinstall dependencies without affecting your settings

### "I can't find my old .env file"
- On Windows: Make sure you can see hidden files (View > Hidden items)
- On Mac: Press Command+Shift+. in Finder
- The file is in the main EmailReader folder

### "I'm completely confused"
- No worries! Just use Option 3 (Start Fresh)
- You'll need to re-enter your email and API key, but it only takes 2 minutes

---

## 💡 What's New in This Update?

- **GoDaddy support** - Now works with GoDaddy-hosted email!
- **Multi-provider support** - Gmail, Outlook, Yahoo, iCloud, and GoDaddy
- **Better error messages** - More helpful when something goes wrong
- **Improved setup wizard** - Easier to configure

---

## Need More Help?

If you're stuck:
1. Check the BEGINNER_GUIDE.md file
2. Create an issue on GitHub
3. Ask someone tech-savvy to help with the update

The update should only take 5-10 minutes! 🚀
