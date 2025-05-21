import os
import logging
import telegram
from telegram import Bot
from asgiref.sync import async_to_sync
from dotenv import load_dotenv


load_dotenv()
logger = logging.getLogger(__name__)

async def async_send_telegram_message(token, chat_id, message, parse_mode="Markdown"):
    try:
        bot = telegram.Bot(token=token)
        await bot.send_message(chat_id=chat_id, text=message, parse_mode=parse_mode)
        logger.info(f'Сообщение отправлено в чат {chat_id}')
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        raise

def send_telegram_message(token, chat_id, message):
    async_to_sync(async_send_telegram_message)(token, chat_id, message)

# send_telegram_message(
#     os.getenv("TELEGRAM_BOT_API_KEY"),
#     os.getenv("TELEGRAM_USER_ID"),
#     "Тестовое сообщение"
# )