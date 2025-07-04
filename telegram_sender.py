import requests
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from pymongo import MongoClient


def send_telegram_message(bot_token, chat_id, message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    response = requests.post(url, data=data)
    print(response.json())

# --- MongoDB Chat ID Storage ---

def get_mongo_collection():
    from dotenv import load_dotenv
    load_dotenv()
    mongo_uri = os.getenv("MONGODB_URI")
    client = MongoClient(mongo_uri)
    db = client["timetablebot"]
    return db["chat_ids"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_chat.id) if update.effective_chat else None
    if not chat_id:
        return
    collection = get_mongo_collection()
    # Only add if not already present
    if not collection.find_one({"chat_id": chat_id}):
        collection.insert_one({"chat_id": chat_id})
        print(f"Added new chat_id: {chat_id}")
    if update.message:
        await update.message.reply_text("You are now subscribed to timetable notifications!")

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_chat.id) if update.effective_chat else None
    if not chat_id:
        return
    collection = get_mongo_collection()
    result = collection.delete_one({"chat_id": chat_id})
    if update.message:
        if result.deleted_count:
            await update.message.reply_text("You have been unsubscribed from timetable notifications.")
        else:
            await update.message.reply_text("You were not subscribed.")

async def run_collector_bot():
    from dotenv import load_dotenv
    load_dotenv()
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not bot_token:
        raise ValueError("TELEGRAM_BOT_TOKEN is not set in environment variables.")
    app = ApplicationBuilder().token(bot_token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop))
    print("Bot is running. Press Ctrl+C to stop.")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    import nest_asyncio
    nest_asyncio.apply()
    asyncio.run(run_collector_bot()) 