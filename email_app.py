"""
Simple GUI application for Email Reader - No coding required!
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import os
from pathlib import Path
import threading
from dotenv import load_dotenv, set_key
from main import run_email_summary


class EmailReaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Email Reader - Daily Summary")
        self.root.geometry("700x600")
        self.root.resizable(False, False)

        # Set icon color scheme
        self.root.configure(bg='#f0f0f0')

        # Load existing config
        self.env_file = Path('.env')
        self.config = self.load_config()

        # Create UI
        self.create_widgets()

        # Check if setup is needed
        if not self.is_configured():
            self.show_setup_wizard()

    def load_config(self):
        """Load configuration from .env file."""
        if self.env_file.exists():
            load_dotenv()
            return {
                'email_address': os.getenv('EMAIL_ADDRESS', ''),
                'email_password': os.getenv('EMAIL_PASSWORD', ''),
                'email_provider': os.getenv('EMAIL_PROVIDER', 'outlook'),
                'imap_server': os.getenv('IMAP_SERVER', 'outlook.office365.com'),
                'imap_port': os.getenv('IMAP_PORT', '993'),
                'smtp_server': os.getenv('SMTP_SERVER', 'smtp.office365.com'),
                'smtp_port': os.getenv('SMTP_PORT', '587'),
                'anthropic_api_key': os.getenv('ANTHROPIC_API_KEY', ''),
                'summary_time': os.getenv('SUMMARY_TIME', '08:00'),
            }
        return {
            'email_address': '',
            'email_password': '',
            'email_provider': 'outlook',
            'imap_server': 'outlook.office365.com',
            'imap_port': '993',
            'smtp_server': 'smtp.office365.com',
            'smtp_port': '587',
            'anthropic_api_key': '',
            'summary_time': '08:00',
        }

    def is_configured(self):
        """Check if app is fully configured."""
        return (self.config['email_address'] and
                self.config['email_password'] and
                self.config['anthropic_api_key'])

    def save_config(self):
        """Save configuration to .env file."""
        if not self.env_file.exists():
            # Create from template
            with open('.env.example', 'r') as f:
                content = f.read()
            with open('.env', 'w') as f:
                f.write(content)

        # Update values
        set_key('.env', 'EMAIL_ADDRESS', self.config['email_address'])
        set_key('.env', 'EMAIL_PASSWORD', self.config['email_password'])
        set_key('.env', 'EMAIL_PROVIDER', self.config['email_provider'])
        set_key('.env', 'IMAP_SERVER', self.config['imap_server'])
        set_key('.env', 'IMAP_PORT', str(self.config['imap_port']))
        set_key('.env', 'SMTP_SERVER', self.config['smtp_server'])
        set_key('.env', 'SMTP_PORT', str(self.config['smtp_port']))
        set_key('.env', 'ANTHROPIC_API_KEY', self.config['anthropic_api_key'])
        set_key('.env', 'SUMMARY_TIME', self.config['summary_time'])

    def create_widgets(self):
        """Create the main application interface."""
        # Header
        header = tk.Frame(self.root, bg='#2c3e50', height=80)
        header.pack(fill='x')

        title = tk.Label(
            header,
            text="📧 Email Reader",
            font=('Arial', 24, 'bold'),
            bg='#2c3e50',
            fg='white'
        )
        title.pack(pady=20)

        # Main content area
        content = tk.Frame(self.root, bg='#f0f0f0')
        content.pack(fill='both', expand=True, padx=20, pady=20)

        # Status section
        status_frame = tk.LabelFrame(
            content,
            text="📊 Status",
            font=('Arial', 12, 'bold'),
            bg='#f0f0f0',
            padx=10,
            pady=10
        )
        status_frame.pack(fill='x', pady=(0, 10))

        if self.is_configured():
            status_text = f"✓ Configured for: {self.config['email_address']}\n✓ Daily summary at: {self.config['summary_time']}"
            status_color = '#27ae60'
        else:
            status_text = "⚠ Not configured yet. Click 'Setup' below."
            status_color = '#e74c3c'

        self.status_label = tk.Label(
            status_frame,
            text=status_text,
            font=('Arial', 10),
            bg='#f0f0f0',
            fg=status_color,
            justify='left'
        )
        self.status_label.pack(anchor='w')

        # Action buttons
        button_frame = tk.Frame(content, bg='#f0f0f0')
        button_frame.pack(fill='x', pady=10)

        # Setup button
        self.setup_btn = tk.Button(
            button_frame,
            text="⚙️ Setup / Change Settings",
            font=('Arial', 11),
            bg='#3498db',
            fg='white',
            activebackground='#2980b9',
            activeforeground='white',
            padx=20,
            pady=10,
            cursor='hand2',
            command=self.show_setup_wizard
        )
        self.setup_btn.pack(fill='x', pady=5)

        # Test button
        self.test_btn = tk.Button(
            button_frame,
            text="🧪 Test Connection",
            font=('Arial', 11),
            bg='#f39c12',
            fg='white',
            activebackground='#e67e22',
            activeforeground='white',
            padx=20,
            pady=10,
            cursor='hand2',
            command=self.test_connection,
            state='normal' if self.is_configured() else 'disabled'
        )
        self.test_btn.pack(fill='x', pady=5)

        # Run now button
        self.run_btn = tk.Button(
            button_frame,
            text="▶️ Send Email Summary Now",
            font=('Arial', 12, 'bold'),
            bg='#27ae60',
            fg='white',
            activebackground='#229954',
            activeforeground='white',
            padx=20,
            pady=15,
            cursor='hand2',
            command=self.run_now,
            state='normal' if self.is_configured() else 'disabled'
        )
        self.run_btn.pack(fill='x', pady=5)

        # Auto-schedule button
        self.schedule_btn = tk.Button(
            button_frame,
            text="🕐 Setup Daily Automatic Sending",
            font=('Arial', 11),
            bg='#9b59b6',
            fg='white',
            activebackground='#8e44ad',
            activeforeground='white',
            padx=20,
            pady=10,
            cursor='hand2',
            command=self.show_schedule_instructions,
            state='normal' if self.is_configured() else 'disabled'
        )
        self.schedule_btn.pack(fill='x', pady=5)

        # Log area
        log_frame = tk.LabelFrame(
            content,
            text="📝 Activity Log",
            font=('Arial', 11, 'bold'),
            bg='#f0f0f0',
            padx=10,
            pady=10
        )
        log_frame.pack(fill='both', expand=True, pady=10)

        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            font=('Courier', 9),
            bg='#ffffff',
            fg='#000000',
            height=10,
            wrap='word',
            state='disabled'
        )
        self.log_text.pack(fill='both', expand=True)

        self.log("Welcome to Email Reader! 👋")
        self.log("This app will send you daily email summaries at 8am.")
        if not self.is_configured():
            self.log("⚠ Please click 'Setup' to get started.")

    def log(self, message):
        """Add a message to the log."""
        self.log_text.configure(state='normal')
        self.log_text.insert('end', f"{message}\n")
        self.log_text.see('end')
        self.log_text.configure(state='disabled')

    def show_setup_wizard(self):
        """Show the setup wizard dialog."""
        wizard = tk.Toplevel(self.root)
        wizard.title("Setup Wizard")
        wizard.geometry("600x550")
        wizard.resizable(False, False)
        wizard.transient(self.root)
        wizard.grab_set()

        # Header
        header = tk.Frame(wizard, bg='#2c3e50', height=60)
        header.pack(fill='x')

        title = tk.Label(
            header,
            text="⚙️ Email Reader Setup",
            font=('Arial', 18, 'bold'),
            bg='#2c3e50',
            fg='white'
        )
        title.pack(pady=15)

        # Content
        content = tk.Frame(wizard, bg='#f0f0f0', padx=30, pady=20)
        content.pack(fill='both', expand=True)

        # Instructions
        instructions = tk.Label(
            content,
            text="Enter your email and API credentials below:",
            font=('Arial', 10),
            bg='#f0f0f0',
            fg='#555'
        )
        instructions.pack(anchor='w', pady=(0, 15))

        # Email Provider Selection
        tk.Label(content, text="📮 Email Provider:", font=('Arial', 10, 'bold'), bg='#f0f0f0').pack(anchor='w')

        provider_frame = tk.Frame(content, bg='#f0f0f0')
        provider_frame.pack(anchor='w', pady=(5, 15), fill='x')

        provider_var = tk.StringVar(value=self.config.get('email_provider', 'outlook'))

        # Provider settings dictionary
        provider_settings = {
            'gmail': {
                'imap_server': 'imap.gmail.com',
                'imap_port': '993',
                'smtp_server': 'smtp.gmail.com',
                'smtp_port': '587',
                'note': 'Use an App Password (not your regular password)'
            },
            'outlook': {
                'imap_server': 'outlook.office365.com',
                'imap_port': '993',
                'smtp_server': 'smtp.office365.com',
                'smtp_port': '587',
                'note': 'Works with @outlook.com, @hotmail.com, and Office 365'
            },
            'yahoo': {
                'imap_server': 'imap.mail.yahoo.com',
                'imap_port': '993',
                'smtp_server': 'smtp.mail.yahoo.com',
                'smtp_port': '587',
                'note': 'Use an App Password (not your regular password)'
            },
            'icloud': {
                'imap_server': 'imap.mail.me.com',
                'imap_port': '993',
                'smtp_server': 'smtp.mail.me.com',
                'smtp_port': '587',
                'note': 'Use an App-Specific Password'
            }
        }

        # Provider dropdown
        provider_dropdown = ttk.Combobox(
            provider_frame,
            textvariable=provider_var,
            values=['gmail', 'outlook', 'yahoo', 'icloud'],
            state='readonly',
            font=('Arial', 11),
            width=20
        )
        provider_dropdown.pack(side='left', padx=(0, 10))

        # Provider note label
        provider_note = tk.Label(
            provider_frame,
            text=provider_settings[provider_var.get()]['note'],
            font=('Arial', 8),
            bg='#f0f0f0',
            fg='#888'
        )
        provider_note.pack(side='left')

        # Update note when provider changes
        def on_provider_change(event):
            selected = provider_var.get()
            provider_note.config(text=provider_settings[selected]['note'])

        provider_dropdown.bind('<<ComboboxSelected>>', on_provider_change)

        # Email Address
        tk.Label(content, text="📧 Your Email Address:", font=('Arial', 10, 'bold'), bg='#f0f0f0').pack(anchor='w')
        email_entry = tk.Entry(content, font=('Arial', 11), width=50)
        email_entry.insert(0, self.config['email_address'])
        email_entry.pack(fill='x', pady=(5, 15))

        # Email Password
        tk.Label(content, text="🔑 Your Email Password:", font=('Arial', 10, 'bold'), bg='#f0f0f0').pack(anchor='w')
        tk.Label(content, text="(Use app-specific password if you have 2FA enabled)", font=('Arial', 8), bg='#f0f0f0', fg='#888').pack(anchor='w')
        password_entry = tk.Entry(content, font=('Arial', 11), width=50, show='*')
        password_entry.insert(0, self.config['email_password'])
        password_entry.pack(fill='x', pady=(5, 15))

        # Show/hide password
        show_password_var = tk.BooleanVar()
        def toggle_password():
            password_entry.config(show='' if show_password_var.get() else '*')

        show_password_check = tk.Checkbutton(
            content,
            text="Show password",
            variable=show_password_var,
            command=toggle_password,
            bg='#f0f0f0'
        )
        show_password_check.pack(anchor='w', pady=(0, 15))

        # Anthropic API Key
        tk.Label(content, text="🤖 Anthropic API Key (for Claude AI):", font=('Arial', 10, 'bold'), bg='#f0f0f0').pack(anchor='w')

        link_frame = tk.Frame(content, bg='#f0f0f0')
        link_frame.pack(anchor='w', pady=(0, 5))

        tk.Label(link_frame, text="Get your API key from:", font=('Arial', 8), bg='#f0f0f0', fg='#888').pack(side='left')

        api_link = tk.Label(link_frame, text="console.anthropic.com", font=('Arial', 8, 'underline'), bg='#f0f0f0', fg='#3498db', cursor='hand2')
        api_link.pack(side='left', padx=5)
        api_link.bind('<Button-1>', lambda e: self.open_url('https://console.anthropic.com/'))

        api_entry = tk.Entry(content, font=('Arial', 11), width=50, show='*')
        api_entry.insert(0, self.config['anthropic_api_key'])
        api_entry.pack(fill='x', pady=(5, 15))

        # Summary Time
        tk.Label(content, text="🕐 What time should I send the daily summary?", font=('Arial', 10, 'bold'), bg='#f0f0f0').pack(anchor='w')

        time_frame = tk.Frame(content, bg='#f0f0f0')
        time_frame.pack(anchor='w', pady=(5, 20))

        time_entry = tk.Entry(time_frame, font=('Arial', 11), width=10)
        time_entry.insert(0, self.config['summary_time'])
        time_entry.pack(side='left')

        tk.Label(time_frame, text="(24-hour format, e.g., 08:00 for 8am)", font=('Arial', 8), bg='#f0f0f0', fg='#888').pack(side='left', padx=10)

        # Save button
        def save_and_close():
            self.config['email_address'] = email_entry.get().strip()
            self.config['email_password'] = password_entry.get().strip()
            self.config['anthropic_api_key'] = api_entry.get().strip()
            self.config['summary_time'] = time_entry.get().strip()

            # Get provider and set server settings
            selected_provider = provider_var.get()
            self.config['email_provider'] = selected_provider
            self.config['imap_server'] = provider_settings[selected_provider]['imap_server']
            self.config['imap_port'] = provider_settings[selected_provider]['imap_port']
            self.config['smtp_server'] = provider_settings[selected_provider]['smtp_server']
            self.config['smtp_port'] = provider_settings[selected_provider]['smtp_port']

            if not all([self.config['email_address'], self.config['email_password'], self.config['anthropic_api_key']]):
                messagebox.showerror("Missing Information", "Please fill in all fields!")
                return

            self.save_config()
            wizard.destroy()

            # Update UI
            self.update_status()
            self.test_btn.config(state='normal')
            self.run_btn.config(state='normal')
            self.schedule_btn.config(state='normal')

            self.log("✓ Configuration saved successfully!")
            messagebox.showinfo("Success!", "Settings saved! You can now test the connection or send a summary.")

        save_btn = tk.Button(
            content,
            text="💾 Save Settings",
            font=('Arial', 12, 'bold'),
            bg='#27ae60',
            fg='white',
            activebackground='#229954',
            activeforeground='white',
            padx=30,
            pady=10,
            cursor='hand2',
            command=save_and_close
        )
        save_btn.pack(pady=10)

    def update_status(self):
        """Update the status label."""
        if self.is_configured():
            status_text = f"✓ Configured for: {self.config['email_address']}\n✓ Daily summary at: {self.config['summary_time']}"
            status_color = '#27ae60'
        else:
            status_text = "⚠ Not configured yet. Click 'Setup' below."
            status_color = '#e74c3c'

        self.status_label.config(text=status_text, fg=status_color)

    def test_connection(self):
        """Test email and API connection."""
        self.log("\n🧪 Testing connection...")
        self.test_btn.config(state='disabled')

        def test_thread():
            try:
                from email_reader import EmailReader
                from anthropic import Anthropic

                # Test email connection
                self.log("→ Testing email connection...")
                reader = EmailReader(
                    email_address=self.config['email_address'],
                    password=self.config['email_password'],
                    imap_server=self.config['imap_server'],
                    imap_port=int(self.config['imap_port'])
                )

                if reader.connect():
                    self.log("  ✓ Email connection successful!")
                    reader.disconnect()
                else:
                    self.log("  ✗ Email connection failed!")
                    self.root.after(0, lambda: messagebox.showerror("Connection Failed", "Could not connect to your email. Check your email and password."))
                    return

                # Test API connection
                self.log("→ Testing Claude API connection...")
                client = Anthropic(api_key=self.config['anthropic_api_key'])

                response = client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=100,
                    messages=[{"role": "user", "content": "Say 'Hello!' in one word."}]
                )

                self.log("  ✓ Claude API connection successful!")
                self.log("\n✅ All tests passed! Everything is working correctly.")

                self.root.after(0, lambda: messagebox.showinfo("Success!", "All connections tested successfully!\n\nYou're ready to use Email Reader."))

            except Exception as e:
                self.log(f"  ✗ Error: {str(e)}")
                self.root.after(0, lambda: messagebox.showerror("Test Failed", f"Connection test failed:\n\n{str(e)}"))
            finally:
                self.root.after(0, lambda: self.test_btn.config(state='normal'))

        threading.Thread(target=test_thread, daemon=True).start()

    def run_now(self):
        """Run the email summary now."""
        result = messagebox.askyesno(
            "Send Summary Now?",
            "This will:\n"
            "1. Read your emails from the last 24 hours\n"
            "2. Create an AI-powered summary\n"
            "3. Email it to you\n\n"
            "Continue?"
        )

        if not result:
            return

        self.log("\n▶️ Starting email summary process...")
        self.run_btn.config(state='disabled')

        def run_thread():
            try:
                self.log("→ Reading emails from last 24 hours...")
                self.log("→ Creating AI summary...")
                self.log("→ Sending summary email...")

                run_email_summary()

                self.log("\n✅ Success! Check your email for the summary.")
                self.root.after(0, lambda: messagebox.showinfo("Success!", "Email summary sent!\n\nCheck your inbox for the summary."))

            except Exception as e:
                self.log(f"\n✗ Error: {str(e)}")
                self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to send summary:\n\n{str(e)}"))
            finally:
                self.root.after(0, lambda: self.run_btn.config(state='normal'))

        threading.Thread(target=run_thread, daemon=True).start()

    def show_schedule_instructions(self):
        """Show instructions for setting up automatic daily sending."""
        instructions_window = tk.Toplevel(self.root)
        instructions_window.title("Setup Automatic Daily Sending")
        instructions_window.geometry("650x600")
        instructions_window.resizable(False, False)
        instructions_window.transient(self.root)
        instructions_window.grab_set()

        # Header
        header = tk.Frame(instructions_window, bg='#9b59b6', height=60)
        header.pack(fill='x')

        title = tk.Label(
            header,
            text="🕐 Setup Automatic Daily Sending",
            font=('Arial', 16, 'bold'),
            bg='#9b59b6',
            fg='white'
        )
        title.pack(pady=15)

        # Content with tabs
        content = tk.Frame(instructions_window, bg='#f0f0f0')
        content.pack(fill='both', expand=True, padx=20, pady=20)

        # Create notebook (tabs)
        notebook = ttk.Notebook(content)
        notebook.pack(fill='both', expand=True)

        # Option 1: Simple Python Scheduler
        simple_tab = tk.Frame(notebook, bg='#ffffff')
        notebook.add(simple_tab, text="🟢 Easy Way (Recommended)")

        simple_content = scrolledtext.ScrolledText(simple_tab, font=('Arial', 10), wrap='word', padx=15, pady=15)
        simple_content.pack(fill='both', expand=True)
        simple_content.insert('1.0', """SIMPLE METHOD - Keep a Window Open

This is the easiest way! Just run the scheduler program:

Step 1: Open a Command Prompt or Terminal

Step 2: Navigate to the Email Reader folder:
   cd path/to/EmailReader

Step 3: Run the scheduler:
   python scheduler.py

Step 4: Keep the window open!
   The program will run in the background and send your
   summary every day at """ + self.config['summary_time'] + """.

   You can minimize the window, but don't close it.

TIP: To stop the scheduler, press Ctrl+C in the window.

IMPORTANT: Your computer must be on and awake at """ + self.config['summary_time'] + """
for the email to be sent!
""")
        simple_content.config(state='disabled')

        # Option 2: Windows Task Scheduler
        windows_tab = tk.Frame(notebook, bg='#ffffff')
        notebook.add(windows_tab, text="🪟 Windows (Advanced)")

        windows_content = scrolledtext.ScrolledText(windows_tab, font=('Arial', 10), wrap='word', padx=15, pady=15)
        windows_content.pack(fill='both', expand=True)

        # Get the current directory
        current_dir = os.getcwd()
        windows_content.insert('1.0', f"""WINDOWS TASK SCHEDULER

This runs automatically even if you're not logged in:

Step 1: Open Task Scheduler
   - Press Windows key
   - Type "Task Scheduler"
   - Click on "Task Scheduler"

Step 2: Create a New Task
   - Click "Create Basic Task" on the right side
   - Name it: "Email Summary"
   - Click "Next"

Step 3: Set Trigger
   - Choose "Daily"
   - Click "Next"
   - Set time to: {self.config['summary_time']}
   - Click "Next"

Step 4: Set Action
   - Choose "Start a program"
   - Click "Next"

   Program/script:
   python

   Add arguments:
   "{current_dir}\\main.py"

   Start in:
   {current_dir}

Step 5: Finish
   - Click "Finish"

Your email summary will now run automatically every day!
""")
        windows_content.config(state='disabled')

        # Option 3: Mac/Linux cron
        mac_tab = tk.Frame(notebook, bg='#ffffff')
        notebook.add(mac_tab, text="🍎 Mac/Linux (Advanced)")

        mac_content = scrolledtext.ScrolledText(mac_tab, font=('Arial', 10), wrap='word', padx=15, pady=15)
        mac_content.pack(fill='both', expand=True)

        current_dir = os.getcwd()
        hour, minute = self.config['summary_time'].split(':')

        mac_content.insert('1.0', f"""MAC/LINUX CRON JOB

This runs automatically in the background:

Step 1: Open Terminal

Step 2: Edit your crontab:
   crontab -e

Step 3: Add this line (press 'i' to insert):
   {minute} {hour} * * * cd {current_dir} && python main.py

Step 4: Save and exit:
   - Press 'Esc'
   - Type ':wq'
   - Press 'Enter'

Your email summary will now run automatically every day at {self.config['summary_time']}!

To check if it was added successfully:
   crontab -l
""")
        mac_content.config(state='disabled')

        # Close button
        close_btn = tk.Button(
            content,
            text="Got it!",
            font=('Arial', 11),
            bg='#27ae60',
            fg='white',
            padx=30,
            pady=8,
            cursor='hand2',
            command=instructions_window.destroy
        )
        close_btn.pack(pady=(10, 0))

    def open_url(self, url):
        """Open a URL in the default browser."""
        import webbrowser
        webbrowser.open(url)


def main():
    """Run the Email Reader GUI application."""
    root = tk.Tk()
    app = EmailReaderApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
