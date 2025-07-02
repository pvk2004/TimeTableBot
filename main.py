import os
from dotenv import load_dotenv
from timetable_parser import parse_excel_timetable
from telegram_sender import send_telegram_message
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

def build_whatsapp_message(day, slots):
    if not slots:
        return f"Good Morning! No classes scheduled for {day}."
    msg = f"Good Morning! Here's your timetable for {day}:\n"
    for start, end, subject in slots:
        # If start or end contains multiple times, only use the first and last
        start_clean = start.split('–')[0].strip()
        end_clean = end.split('–')[-1].strip()
        msg += f"- {start_clean} – {end_clean}: {subject}\n"
    return msg.strip()

if __name__ == "__main__":
    now = datetime.now()
    timetable = parse_excel_timetable("timetable.xlsx")
    today = now.strftime("%A").upper()
    slots = timetable.get(today) or timetable.get(today.title()) or []
    message = build_whatsapp_message(today.title(), slots)
    print(message)

    # Read Telegram bot token and chat IDs from environment variables
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_ids = os.getenv("TELEGRAM_CHAT_IDS", "").split(",")
    chat_ids = [cid.strip() for cid in chat_ids if cid.strip()]

    for chat_id in chat_ids:
        send_telegram_message(bot_token, chat_id, message)

