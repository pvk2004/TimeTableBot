import os
from dotenv import load_dotenv
from timetable_parser import parse_excel_timetable
from telegram_sender import send_telegram_message
from datetime import datetime, time

# Load environment variables from .env file
load_dotenv()

def get_current_subject(slots, now):
    # now is a datetime object
    for start, end, subject in slots:
        try:
            # Try parsing times in both 12-hour and 24-hour formats
            try:
                start_dt = datetime.strptime(start.strip(), "%I:%M %p")
                end_dt = datetime.strptime(end.strip(), "%I:%M %p")
            except ValueError:
                start_dt = datetime.strptime(start.strip(), "%H:%M")
                end_dt = datetime.strptime(end.strip(), "%H:%M")
        except Exception:
            continue  # skip if time format is not as expected
        # Replace the date with today's date for comparison
        start_dt = start_dt.replace(year=now.year, month=now.month, day=now.day)
        end_dt = end_dt.replace(year=now.year, month=now.month, day=now.day)
        if start_dt.time() <= now.time() < end_dt.time():
            return f"Current class: {subject} ({start} – {end})"
    return None

if __name__ == "__main__":
    now = datetime.now()
    # Define timetable hours (e.g., 8:00 to 18:00)
    timetable_start = time(9, 0)
    timetable_end = time(16, 0)
    if not (timetable_start <= now.time() < timetable_end):
        print("Outside timetable hours. No message sent.")
        exit(0)

    timetable = parse_excel_timetable("timetable.xlsx")
    today = now.strftime("%A").upper()
    slots = timetable.get(today) or timetable.get(today.title()) or []
    message = get_current_subject(slots, now)
    if message:
        print(message)
        bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
        chat_ids = os.environ.get("TELEGRAM_CHAT_IDS", "").split(",")
        chat_ids = [cid.strip() for cid in chat_ids if cid.strip()]
        for chat_id in chat_ids:
            send_telegram_message(bot_token, chat_id, message)
    else:
        print("No class scheduled for this hour. No message sent.") 