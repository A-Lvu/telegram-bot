import os
from dotenv import load_dotenv
from telegram_bot.logging import LOGGER
from telegram_bot.bot import Bot


load_dotenv()
TOKEN = os.getenv("TOKEN")


if __name__ == '__main__':
    LOGGER.info("Start MAIN")
    _myBot = Bot(token=TOKEN)
    