# 📅 TimeTableBot 

TimeTableBot is a Telegram bot that automatically sends you your class timetable for the day and can send reminders for each class as it starts. Designed for students who want daily and hourly schedule notifications—completely free using Telegram!

---

## 🚀 Features

- 📆 Sends daily class timetable every morning at 8:00 AM (IST)
- ⏰ Sends reminders at the start of each class (no spam during long labs)
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
2. **Get Your Chat ID:**

   - Start your bot (send /start)
   - Use [@userinfobot](https://t.me/userinfobot) to get your chat ID
3. **Create a `.env` file:**

```
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_IDS=your_chat_id1,your_chat_id2
```

- You can add multiple chat IDs, separated by commas.

4. **Prepare your timetable:**
   - Use `timetable.xlsx` (first column: Day, then time slots as columns)

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

  (Sends a reminder only at the start of each class)

---

## ☁️ Automation with GitHub Actions

You can automate both scripts for free using GitHub Actions:

- **Daily Timetable:** Runs every day at 8:00 AM IST
- **Hourly Reminders:** Runs every hour during timetable hours, but only sends a message at class change

See `.github/workflows/` for ready-to-use workflow files.

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
