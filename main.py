import os
from dotenv import load_dotenv
from timetable_parser import parse_excel_timetable
from whatsapp_sender import send_whatsapp_message_twilio
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
    # Only send at 8:00 AM
    # if now.hour == 8 and now.minute == 0:
    timetable = parse_excel_timetable("timetable.xlsx")
    today = now.strftime("%A").upper()
    slots = timetable.get(today) or timetable.get(today.title()) or []
    message = build_whatsapp_message(today.title(), slots)
    print(message)

        # Read Twilio credentials and WhatsApp numbers from environment variables
    account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
    auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
    from_whatsapp_number = os.environ.get("TWILIO_FROM_WHATSAPP")
    to_whatsapp_numbers = os.environ.get("TWILIO_TO_WHATSAPP_LIST", "").split(",")
    to_whatsapp_numbers = [num.strip() for num in to_whatsapp_numbers if num.strip()]

    for to_whatsapp_number in to_whatsapp_numbers:
        send_whatsapp_message_twilio(account_sid, auth_token, from_whatsapp_number, to_whatsapp_number, message)
    # else:
        # print("Not 8:00 AM. No message sent.")
