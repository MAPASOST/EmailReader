"""
Scheduler script to run email summary at specified time daily.
"""
import schedule
import time
import os
from dotenv import load_dotenv
from main import run_email_summary
from datetime import datetime


def job_wrapper():
    """Wrapper function to run the email summary job with error handling."""
    try:
        run_email_summary()
    except Exception as e:
        print(f"Job failed with error: {e}")


def start_scheduler():
    """
    Start the scheduler to run email summary daily at specified time.
    """
    load_dotenv()

    # Get summary time from environment (default: 08:00)
    summary_time = os.getenv('SUMMARY_TIME', '08:00')

    print(f"\n{'='*60}")
    print("Email Reader Scheduler Started")
    print(f"{'='*60}")
    print(f"Summary will be sent daily at: {summary_time}")
    print(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Press Ctrl+C to stop the scheduler")
    print(f"{'='*60}\n")

    # Schedule the job
    schedule.every().day.at(summary_time).do(job_wrapper)

    # Keep the script running
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        print("\n\nScheduler stopped by user.")


if __name__ == "__main__":
    start_scheduler()
