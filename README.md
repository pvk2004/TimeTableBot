# 📅 TimeTableBot 

TimeTableBot is a Telegram bot that automatically sends you your class timetable for the day and can send reminders for each class as it starts. Designed for students who want daily and hourly schedule notifications—completely free using Telegram!

---

## 🚀 Features

- 📆 Sends daily class timetable every morning at 8:00 AM (IST, with a 20-minute window)
- ⏰ Sends reminders 5 minutes before each class starts (no spam during long labs or continuous same classes)
- 🗓 Loads timetable from an Excel file (`timetable.xlsx`)
- 🤖 100% free using Telegram Bot API
- ☁️ Automated with Render (no server management needed)

---

## 📦 Installation (Local Development)

```bash
git clone https://github.com/pvk2004/TimeTableBot.git
cd TimeTableBot
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## ⚙️ Configuration

1. **Create a Telegram Bot:**
   - Message [@BotFather](https://t.me/BotFather) on Telegram
   - Use `/newbot` and follow the instructions
   - Save your bot token
2. **Automatic Chat ID Collection:**
   - Run the bot manually (see below) and send `/start` on Telegram.
   - The bot will automatically collect your chat ID and store it in MongoDB.
   - To unsubscribe, send `/stop` to the bot.
3. **Set up Environment Variables:**

For local development, create a `.env` file:
```
TELEGRAM_BOT_TOKEN=your_bot_token_here
MONGODB_URI=your_mongodb_atlas_uri_here
```

For Render, set both `TELEGRAM_BOT_TOKEN` and `MONGODB_URI` as environment variables in the Render dashboard.

---

## ▶️ Usage

- **Collect Chat IDs (Manual):**
  - Run the bot manually whenever you want to allow users to subscribe/unsubscribe:
    ```bash
    python telegram_sender.py
    ```
  - Users send `/start` to subscribe and `/stop` to unsubscribe.

- **Daily Timetable (Automated):**
  - On Render, a scheduled worker runs `main.py` every morning.
  - The script sends the timetable to all users **between 7:50 and 8:10 AM IST**.

- **Hourly/Class Change Reminders (Automated):**
  - On Render, a scheduled worker runs `hourly_reminder.py` every 5 minutes.
  - The script sends reminders **5 minutes before each class** (only between **9:00 and 16:00 IST**).
  - No spamming for long labs or continuous same classes.

---

## ☁️ Deploying on Render

1. [Sign up for Render](https://render.com).
2. Click "New Blueprint" and connect your repo.
3. Render will detect `render.yaml` and set up services:
   - **Web Service**: For Telegram bot chat ID collection.
   - **Workers**: For daily and hourly timetable notifications.
4. Set the environment variables `TELEGRAM_BOT_TOKEN` and `MONGODB_URI` in the Render dashboard.
5. Upload your `timetable.xlsx` file in the Render dashboard or commit it to your repo.

---

## 🛠 Render Automation

- **No need for a 24/7 server or Railway/Heroku.**
- All notifications are sent by scheduled Render background workers.
- See `render.yaml` for details.

---

## 🕒 Timezone Support
- All time calculations use **IST (Asia/Kolkata)**.
- The project uses the `pytz` library for timezone handling (see `requirements.txt`).

---

## 📨 Sample Hourly Reminder Output

```
Upcoming class in 5 minutes: Physics (10:00 AM – 11:00 AM)
```

---

## 🗂 Timetable Format (Excel)

- The Excel file should have days as rows and time slots as columns:

| Day     | 9:00 AM – 10:00 AM | 10:00 AM – 11:00 AM | ... |
| ------- | ------------------- | -------------------- | --- |
| Monday  | Math                | Physics              | ... |
| Tuesday | ...                 | ...                  | ... |

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a new branch: `git checkout -b feature-name`
3. Make your changes and commit: `git commit -m "Add feature"`
4. Push to your fork: `git push origin feature-name`
5. Create a Pull Request

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

---

## 🙋‍♂️ Author

Made  by [pvk2004](https://github.com/pvk2004)
