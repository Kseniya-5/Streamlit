import os
from  dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')
API_W = os.getenv('API_WEATHER')
if not TOKEN:
    raise ValueError('Переменная окружения BOT_TOKEN не установлена!')
elif not API_W:
    raise ValueError('Переменная окружения API_WEATHER не установлена!')