import os
from dotenv import load_dotenv
from timetable_parser import parse_excel_timetable
from telegram_sender import send_telegram_message
from datetime import datetime, time, timedelta, timezone
from pymongo import MongoClient

# Load environment variables from .env file (for local dev; in GitHub Actions, secrets are set as env vars)
load_dotenv()

def get_today_timetable_message(timetable, today):
    slots = timetable.get(today) or timetable.get(today.title()) or []
    if not slots:
        return "No classes scheduled for today!\n~~~Happy Holiday!~~~"
    msg = f"Today's Timetable ({today}):\n"
    for start, end, subject in slots:
        msg += f"{start} – {end}: {subject}\n"
    return msg.strip()

def get_chat_ids_from_mongo():
    mongo_uri = os.getenv("MONGODB_URI")
    client = MongoClient(mongo_uri)
    db = client["timetablebot"]
    collection = db["chat_ids"]
    return [doc["chat_id"] for doc in collection.find()]

def check_if_already_sent_today():
    mongo_uri = os.getenv("MONGODB_URI")
    client = MongoClient(mongo_uri)
    db = client["timetablebot"]
    collection = db["daily_sent"]
    today = datetime.now().strftime("%Y-%m-%d")
    return collection.find_one({"date": today}) is not None

def mark_as_sent_today():
    mongo_uri = os.getenv("MONGODB_URI")
    client = MongoClient(mongo_uri)
    db = client["timetablebot"]
    collection = db["daily_sent"]
    today = datetime.now().strftime("%Y-%m-%d")
    collection.insert_one({"date": today, "sent_at": datetime.now()})

if __name__ == "__main__":
    now = datetime.now(timezone.utc)
    # Only send between 2:00 and 3:00 AM UTC
    send_window_start = time(1, 0)
    send_window_end = time(2, 30)
    print(f"Current UTC time: {now.time()}, send window: {send_window_start} to {send_window_end}")
    if not (send_window_start <= now.time() < send_window_end):
        print("Not in 2:00-3:00 AM UTC window. No message sent.")
        exit(0)

    # Check if already sent today
    if check_if_already_sent_today():
        print("Daily timetable already sent today. No message sent.")
        exit(0)

    timetable = parse_excel_timetable("timetable.xlsx")
    today = now.strftime("%A").upper()
    message = get_today_timetable_message(timetable, today)
    chat_ids = get_chat_ids_from_mongo()
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not bot_token:
        print("TELEGRAM_BOT_TOKEN not set. Exiting.")
        exit(1)
    if not chat_ids:
        print("No chat IDs found. Exiting.")
        exit(0)
    
    # Send message to all users
    for chat_id in chat_ids:
        send_telegram_message(bot_token, chat_id, message)
    
    # Mark as sent today
    mark_as_sent_today()
    print("Daily timetable sent successfully.")

