from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
import aiohttp

router = Router()

# Обработчик команды /start
@router.message(Command('start'))
async def cmd_start(message: Message):
    await message.reply('Добро пожаловать! Я Ваш бот.\n'
                        'Введите /help для списка команд.')

# Обработчик команды /help
@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.reply(
        'Доступные команды:\n'
        '/set_profile - Настройка профиля пользователя\n'
        '/log_water - Логирование воды\n'
        '/log_food - Логирование еды\n'
        '/log_workout - Логирование тренировок\n'
        '/check_progress -  Прогресс по воде и калориям'
    )