from aiogram import Router
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command

router = Router()

# Обработчик команды /start
@router.message(Command('start'))
async def cmd_start(message: Message):
    welcome_message = await message.reply(
        f'Добро пожаловать, {message.from_user.first_name}! Я Ваш бот.\n'
        '\nВведите /help для того, чтобы узнать дополнительную информацию о командах.'
    )
    # Автоматически вызываем команду show_keyboard
    await show_keyboard(welcome_message)

# Обработчик команды /help
@router.message(Command('help'))
async def cmd_help(message: Message):
    help_message = await message.reply(
        'Доступные команды:\n'
        '1. Настройка профиля - Обновляет данные: вес (в кг), рост (в см), возраст и т.д.\n'
        '2. Вода - Сохраняет выпитое количество воды и показывает, сколько осталось до нормы.\n'
        '3. Еда - Сохраняет калорийность продукта.\n'
        '4. Тренировка - Фиксирует сожженные калории, учитывает расходы воды на тренировке.\n'
        '5. Прогресс - Показывает прогресс по воде и калориям.'
    )
    # Автоматически вызываем команду show_keyboard
    await show_keyboard(help_message)

# Обработчик команды /keyboard с инлайн-кнопками
async def show_keyboard(message: Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Настройка профиля', callback_data='profile'),
                InlineKeyboardButton(text='Вода', callback_data='water'),
            ],
            [
                InlineKeyboardButton(text='Еда', callback_data='food'),
                InlineKeyboardButton(text='Тренировка', callback_data='training'),
            ],
            [InlineKeyboardButton(text='Прогресс', callback_data='progress')]
        ]
    )
    await message.bot.edit_message_reply_markup(
        chat_id=message.chat.id,
        message_id=message.message_id,
        reply_markup=keyboard
    )

# Обработчик нажатий на инлайн-кнопки
@router.callback_query()
async def handle_callback(callback_query):
    if callback_query.data == 'profile':
        await callback_query.message.reply('Вы выбрали кнопку "Настройка профиля".')
    elif callback_query.data == 'water':
        await callback_query.message.reply('Вы выбрали кнопку "Вода".')
    elif callback_query.data == 'food':
        await callback_query.message.reply('Вы выбрали кнопку "Еда".')
    elif callback_query.data == 'training':
        await callback_query.message.reply('Вы выбрали кнопку "Тренировка".')
    elif callback_query.data == 'progress':
        await callback_query.message.reply('Вы выбрали кнопку "Прогресс".')
    else:
        await callback_query.message.reply('Неизвестная опция.')