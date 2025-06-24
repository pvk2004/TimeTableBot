# 📅 TimeTableBot

TimeTableBot is a Telegram bot that automatically sends users their class timetable based on the current day. It is designed to save time for students who need quick access to their daily or weekly class schedules.

---

## 🚀 Features

- 📆 Sends daily class timetable
- ⏱ Shows upcoming classes with `/next`
- 🗓 View today's schedule with `/today`
- 🤖 Simple Telegram bot interface
- 🧾 Loads timetable from CSV or database (configurable)

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

Edit `config.py` or create a `.env` file with your Telegram bot token:

```python
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
DATA_FILE = "timetable.csv"
```

You can also use a database if your project supports it. Update the data source in the code accordingly.

---

## ▶️ Usage

Start the bot with:

```bash
python main.py
```

Then, open Telegram and interact with your bot:

| Command     | Description                    |
|-------------|--------------------------------|
| `/start`    | Start the bot and register     |
| `/today`    | Get today's timetable          |
| `/next`     | Get the next upcoming class    |

---

## 🗂 Timetable Format (CSV)

If using a CSV file as the data source, make sure it follows this format:

```csv
day,start_time,end_time,subject,room
Monday,09:00,10:00,Math,Room 101
Tuesday,10:00,11:00,Physics,Room 203
...
```

---

## 🐳 Docker Support (Optional)

To run the bot in Docker:

**Dockerfile:**
```dockerfile
FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
```

**Build and run:**
```bash
docker build -t timetablebot .
docker run -e BOT_TOKEN=<your_token> timetablebot
```

---

## 🤝 Contributing

Contributions are welcome!  
To contribute:

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

Made with ❤️ by [pvk2004](https://github.com/pvk2004)
