import os
from dotenv import load_dotenv

load_dotenv()

# Отримуємо токен з файлу .env
TOKEN = os.getenv("BOT_TOKEN")