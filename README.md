# 📅 TimeTableBot 

TimeTableBot is a Telegram bot that automatically sends you your class timetable for the day and can send reminders for each class as it starts. Designed for students who want daily and hourly schedule notifications—completely free using Telegram!

---

## 🚀 Features

- 📆 Sends daily class timetable every morning at 8:00 AM (IST)
- ⏰ Sends reminders 5 minutes before each class starts (no spam during long labs)
- 🗓 Loads timetable from an Excel file (`timetable.xlsx`)
- 🤖 100% free using Telegram Bot API
- ☁️ Can be automated with GitHub Actions (no server needed)

---

## 📦 Installation

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

   - Start your bot (send /start) on Telegram.
   - The bot will automatically collect your chat ID and store it in `chat_ids.txt`.
   - No need to manually edit any files for chat IDs.
   - To unsubscribe, contact the bot admin or (optionally) implement a /stop command.
3. **Set up Environment Variables:**

For local development, create a `.env` file:
```
TELEGRAM_BOT_TOKEN=your_bot_token_here
MONGODB_URI=your_mongodb_atlas_uri_here
```

For GitHub Actions, add both `TELEGRAM_BOT_TOKEN` and `MONGODB_URI` as repository secrets in your GitHub repo settings.

---

## 🛠 Running the Collector Bot

To collect chat IDs automatically, run the following in your terminal:

```python
import asyncio
from telegram_sender import run_collector_bot
asyncio.run(run_collector_bot())
```

Leave this running so users can subscribe by sending /start to your bot. All chat IDs will be saved in `chat_ids.txt`.

---

## 🚂 Deploying the Collector Bot on Railway

1. Push your code to GitHub.
2. Create a new Railway project and link your repo.
3. Add environment variables: `TELEGRAM_BOT_TOKEN` and `MONGODB_URI`.
4. Railway will automatically install dependencies from `requirements.txt` before running your bot.
5. Set the Start Command to:
   ```
   python run_telegram_collector.py
   ```
6. If dependencies are not installed automatically, add a `Procfile` with:
   ```
   release: pip install -r requirements.txt
   start: python run_telegram_collector.py
   ```
   or manually run `pip install -r requirements.txt` in the Railway shell before starting.

Check Railway logs to ensure your bot starts and dependencies are installed.

---

## ▶️ Usage

- **Daily Timetable:**

  ```bash
  python main.py
  ```

  (Sends today's full timetable at 8:00 AM)
- **Hourly/Class Change Reminders:**

  ```bash
  python hourly_reminder.py
  ```

  (Sends a reminder 5 minutes before each class starts)

---

## ☁️ GitHub Actions Automation

All scripts are designed to work seamlessly with GitHub Actions:

- **Daily Timetable:** Runs every day at 8:00 AM IST
- **Hourly Reminders:** Runs every 5 minutes during timetable hours, but only sends a message 5 minutes before each class starts

**How it works:**
The scripts fetch all chat IDs from MongoDB Atlas, so all subscribed users (via /start) will receive notifications.
You must add both `TELEGRAM_BOT_TOKEN` and `MONGODB_URI` as repository secrets in your GitHub repo settings.

See `.github/workflows/` for ready-to-use workflow files. No manual chat ID management is needed.

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
