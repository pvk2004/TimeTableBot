import nest_asyncio
nest_asyncio.apply()

import asyncio
from telegram_sender import run_collector_bot

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(run_collector_bot()) 