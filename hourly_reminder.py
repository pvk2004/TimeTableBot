import os
from dotenv import load_dotenv
from timetable_parser import parse_excel_timetable
from telegram_sender import send_telegram_message
from datetime import datetime, time, timedelta
from pymongo import MongoClient
import pytz

# Load environment variables from .env file (for local dev; in GitHub Actions, secrets are set as env vars)
load_dotenv()

# Set IST timezone
IST = pytz.timezone('Asia/Kolkata')

def get_upcoming_subject(slots, now, advance_minutes=5, window_minutes=5):
    for start, end, subject in slots:
        for fmt in ("%I:%M %p", "%H:%M"):
            try:
                start_dt = datetime.strptime(start.strip(), fmt)
                break
            except ValueError:
                continue
        else:
            continue  # skip if time format is not as expected

        # Set the date and timezone for the slot
        start_dt = IST.localize(start_dt.replace(year=now.year, month=now.month, day=now.day))
        # Calculate the window: [start_dt - advance_minutes, start_dt - advance_minutes + window_minutes)
        window_start = start_dt - timedelta(minutes=advance_minutes)
        window_end = window_start + timedelta(minutes=window_minutes)
        # Only send if now is in the window
        if window_start <= now < window_end:
            return f"Upcoming class in {advance_minutes} minutes: {subject} ({start} – {end})"
    return None

def get_chat_ids_from_mongo():
    mongo_uri = os.getenv("MONGODB_URI")
    client = MongoClient(mongo_uri)
    db = client["timetablebot"]
    collection = db["chat_ids"]
    return [doc["chat_id"] for doc in collection.find()]

if __name__ == "__main__":
    # Always use IST for all time calculations
    now = datetime.now(IST)
    print(f"Current IST time: {now}")
    # Define timetable hours (9:00 to 16:00 IST)
    timetable_start = time(9, 0)
    timetable_end = time(16, 0)
    if not (timetable_start <= now.time() <= timetable_end):
        print("Outside timetable hours (9:00-16:00 IST). No message sent.")
        exit(0)

    timetable = parse_excel_timetable("timetable.xlsx")
    today = now.strftime("%A").upper()
    slots = timetable.get(today) or timetable.get(today.title()) or []
    print(f"Today's slots: {slots}")
    message = get_upcoming_subject(slots, now, advance_minutes=5, window_minutes=5)
    chat_ids = get_chat_ids_from_mongo()
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not bot_token:
        print("TELEGRAM_BOT_TOKEN not set.")
        exit(1)
    if not chat_ids:
        print("No chat IDs found.")
        exit(0)
    if message:
        print(message)
        for chat_id in chat_ids:
            send_telegram_message(bot_token, chat_id, message)
    else:
        print("No class starting at this time. No message sent.") 
