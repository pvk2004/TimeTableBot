import os
from dotenv import load_dotenv
from timetable_parser import parse_excel_timetable
from telegram_sender import send_telegram_message
from datetime import datetime, time

# Load environment variables from .env file
load_dotenv()

def get_starting_subject(slots, now):
    # now is a datetime object
    now_str_12 = now.strftime("%I:%M %p").lstrip('0')  # e.g., '9:00 AM'
    now_str_24 = now.strftime("%H:%M")                 # e.g., '09:00'
    for start, end, subject in slots:
        # Compare with both 12-hour and 24-hour formats
        if start.strip().lstrip('0') == now_str_12 or start.strip() == now_str_24:
            return f"Class starting now: {subject} ({start} – {end})"
    return None

if __name__ == "__main__":
    now = datetime.now()
    # Define timetable hours (e.g., 9:00 to 16:00)
    timetable_start = time(9, 0)
    timetable_end = time(16, 0)
    if not (timetable_start <= now.time() < timetable_end):
        print("Outside timetable hours. No message sent.")
        exit(0)

    timetable = parse_excel_timetable("timetable.xlsx")
    today = now.strftime("%A").upper()
    slots = timetable.get(today) or timetable.get(today.title()) or []
    message = get_starting_subject(slots, now)
    if message:
        print(message)
        bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
        chat_ids = os.environ.get("TELEGRAM_CHAT_IDS", "").split(",")
        chat_ids = [cid.strip() for cid in chat_ids if cid.strip()]
        for chat_id in chat_ids:
            send_telegram_message(bot_token, chat_id, message)
    else:
        print("No class starting at this time. No message sent.") 