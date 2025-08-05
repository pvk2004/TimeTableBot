import os
import threading
import requests
import asyncio # <-- Import asyncio
from dotenv import load_dotenv
from flask import Flask
from pymongo import MongoClient
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from timetable_parser import parse_excel_timetable # Your existing parser

# --- 1. SETUP ---
load_dotenv()
server = Flask(__name__)
# Use a specific timezone for accurate scheduling
scheduler = BackgroundScheduler(timezone="Asia/Kolkata")

@server.route('/')
def home():
    """A simple endpoint to keep the Render service alive."""
    return "Bot is alive and running."

# --- 2. DATABASE & SHARED FUNCTIONS ---
def get_mongo_collection(collection_name):
    """Connects to MongoDB and returns a specific collection."""
    mongo_uri = os.getenv("MONGODB_URI")
    client = MongoClient(mongo_uri)
    db = client["timetablebot"]
    return db[collection_name]

# --- 3. INTERACTIVE BOT LOGIC (/start, /stop) ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Subscribes a user to all notifications."""
    chat_id = str(update.effective_chat.id)
    collection = get_mongo_collection("chat_ids") # Using one central collection
    if not collection.find_one({"chat_id": chat_id}):
        collection.insert_one({"chat_id": chat_id})
        print(f"Added new subscriber: {chat_id}")
    await update.message.reply_text("Welcome! You are now subscribed to all timetable notifications.")

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Unsubscribes a user."""
    chat_id = str(update.effective_chat.id)
    collection = get_mongo_collection("chat_ids")
    collection.delete_one({"chat_id": chat_id})
    await update.message.reply_text("You have been unsubscribed from all notifications.")

# --- 4. SCHEDULED JOB LOGIC (Daily & Hourly) ---

def send_daily_job():
    """Scheduled job to send the full daily timetable."""
    print("SCHEDULER: Running daily timetable job...")
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_ids = [doc["chat_id"] for doc in get_mongo_collection("chat_ids").find()]
    if not bot_token or not chat_ids:
        return

    timetable = parse_excel_timetable("timetable.xlsx")
    today = datetime.now(scheduler.timezone).strftime("%A")
    slots = timetable.get(today) or timetable.get(today.title()) or []

    if not slots:
        message = "No classes scheduled for today! Enjoy your day!"
    else:
        message = f"Today's Timetable ({today}):\n"
        for start, end, subject in slots:
            message += f"\n- {subject} ({start} – {end})"

    for chat_id in chat_ids:
        send_telegram_message(bot_token, chat_id, message)
    print("SCHEDULER: Daily job finished.")

def send_hourly_job():
    """Scheduled job to send reminders for upcoming classes."""
    print(f"SCHEDULER: Running hourly check at {datetime.now(scheduler.timezone).time()}...")
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_ids = [doc["chat_id"] for doc in get_mongo_collection("chat_ids").find()]
    if not bot_token or not chat_ids:
        return

    timetable = parse_excel_timetable("timetable.xlsx")
    now_local = datetime.now(scheduler.timezone)
    today = now_local.strftime("%A")
    slots = timetable.get(today) or timetable.get(today.title()) or []

    message = get_upcoming_subject(slots, now_local)
    if message:
        print(f"SCHEDULER: Found upcoming class. Sending message: {message}")
        for chat_id in chat_ids:
            send_telegram_message(bot_token, chat_id, message)
        print("SCHEDULER: Hourly job finished.")

def get_upcoming_subject(slots, now, advance_minutes=5):
    """Finds the next class starting soon."""
    for start, end, subject in slots:
        # Tries to parse time in different formats
        for fmt in ("%I:%M %p", "%H:%M"):
            try:
                start_dt = datetime.strptime(start.strip(), fmt).time()
                break
            except ValueError:
                continue
        else:
            continue

        # Combine today's date with the class start time
        start_datetime = now.replace(hour=start_dt.hour, minute=start_dt.minute, second=0, microsecond=0)
        
        # Check if 'now' is within the 5-minute window before the class starts
        if now >= (start_datetime - timedelta(minutes=advance_minutes)) and now < start_datetime:
             return f"🔔 Upcoming class in {advance_minutes} minutes: {subject} ({start} – {end})"
    return None

def send_telegram_message(bot_token, chat_id, message):
    """Utility function to send a message via HTTP request."""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"Error sending message to {chat_id}: {e}")


# --- 5. APPLICATION RUNNERS ---

# THIS IS THE CORRECTED FUNCTION
def run_bot():
    """Starts the interactive Telegram bot in a background thread."""
    # Create and set a new event loop for this thread
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    app = ApplicationBuilder().token(bot_token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop))
    print("BOT: Starting polling...")
    app.run_polling()

def run_web_server():
    """Starts the Flask web server to keep the Render service alive."""
    port = int(os.environ.get('PORT', 5000))
    server.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    # Start the bot in a separate thread
    bot_thread = threading.Thread(target=run_bot)
    # bot_thread.daemon = True
    # bot_thread.start()
    
    # # Add jobs to the scheduler
    # # Daily job at 8:00 AM IST
    # scheduler.add_job(send_daily_job, 'cron', day_of_week='mon-sat', hour=8, minute=0)
    # # Hourly job every 5 minutes between 9 AM and 5 PM IST
    # scheduler.add_job(send_hourly_job, 'cron', day_of_week='mon-sat', hour='9-17', minute='*/5')
    
    # scheduler.start()
    # print("SCHEDULER: Started. Jobs are scheduled.")

    # Start the web server in the main thread
    print("SERVER: Starting Flask server...")
    run_web_server()