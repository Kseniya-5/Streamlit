from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.filters import Command
from states import Profile

router = Router()

# Обработчик команды /start
@router.message(Command('start'))
async def cmd_start(message: Message):
    welcome_message = await message.reply(
        f'Добро пожаловать! Я Ваш бот.\n'
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
async def handle_callback(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.data == 'profile':
        await callback_query.message.reply('Вы выбрали кнопку "Настройка профиля".')
        await start_profile(callback_query.message, state)
    elif callback_query.data == 'water':
        await callback_query.message.reply('Вы выбрали кнопку "Вода".')
    elif callback_query.data == 'food':
        await callback_query.message.reply('Вы выбрали кнопку "Еда".')
    elif callback_query.data == 'training':
        await callback_query.message.reply('Вы выбрали кнопку "Тренировка".')
    elif callback_query.data == 'progress':
        await callback_query.message.reply('Вы выбрали кнопку "Прогресс".')

###################################Profile##############################################
async def start_profile(message: Message, state: FSMContext):
    await message.answer('Как Вас зовут?')
    await state.set_state(Profile.name)

@router.callback_query()
async def handle_name_choice(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.data == 'use_telegram_name':
        name = callback_query.from_user.first_name
        await state.update_data(name=name)
        await callback_query.message.answer(f'Ваше имя установлено как {name}. Сколько Вам лет?')
        await state.set_state(Profile.age)

    elif callback_query.data == 'manual_name':
        await callback_query.message.answer('Пожалуйста, введите ваше имя:')
        await state.set_state(Profile.name)

@router.message(Profile.name)
async def process_manual_name(message: Message, state: FSMContext):
    name = message.text.strip()
    if not name:
        await message.answer("Имя не может быть пустым. Пожалуйста, введите ваше имя:")
        return
    await state.update_data(name=name)
    await message.answer('Сколько Вам лет?')
    await state.set_state(Profile.age)


@router.message(Profile.age)
async def process_age(message: Message, state: FSMContext):
    age = message.text.strip()
    # Проверка корректности возраста
    if not age.isdigit() or not (0 < int(age) < 120):
        await message.answer('Пожалуйста, введите корректный возраст (число от 1 до 119):')
        return
    await state.update_data(age=int(age))
    await message.answer('Пожалуйста, укажите свой вес (в кг):')
    await state.set_state(Profile.weight)


@router.message(Profile.weight)
async def process_weight(message: Message, state: FSMContext):
    weight = message.text.strip()
    # Проверка корректности веса
    if not weight.isdigit() or not (0 < float(weight) < 500):
        await message.answer('Пожалуйста, введите корректный вес (число от 1 до 499):')
        return
    await state.update_data(weight=float(weight))
    await message.answer('Пожалуйста, укажите свой рост (в см):')
    await state.set_state(Profile.height)


@router.message(Profile.height)
async def process_height(message: Message, state: FSMContext):
    height = message.text.strip()
    # Проверка корректности роста
    if not height.isdigit() or not (0 < float(height) < 300):
        await message.answer('Пожалуйста, введите корректный рост (число от 1 до 299):')
        return
    await state.update_data(height=int(height))
    await message.answer('Сколько минут активности у вас в день?')
    await state.set_state(Profile.activity_level)

@router.message(Profile.activity_level)
async def process_activity_level(message: Message, state: FSMContext):
    activity_level = message.text.strip()
    if not activity_level.isdigit() or not (0 < int(activity_level) < 1440):
        await message.answer('Пожалуйста, введите корректное время (число от 0 до 1440):')
        return
    await state.update_data(activity_level=message.text)
    await message.answer('В каком городе вы находитесь?')
    await state.set_state(Profile.city)

@router.message(Profile.city)
async def process_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    await message.answer('Какова ваша цель калорий?\n'
                         '(Введите "по умолчанию", чтобы использовать расчет.)')
    await state.set_state(Profile.calorie_goal)


@router.message(Profile.calorie_goal)
async def process_calorie_goal(message: Message, state: FSMContext):
    data = await state.get_data()

    if message.text.lower() == "по умолчанию":
        weight = float(data.get("weight", 0))
        height = float(data.get("height", 0))
        age = int(data.get("age", 0))
        activity_level = float(data.get("activity_level", 0))

        # Расчет калорий по формуле
        calories = 10 * weight + 6.25 * height - 5 * age
        # Добавляем уровень активности
        if activity_level < 30:
            calories += 200
        elif activity_level < 60:
            calories += 300
        else:
            calories += 400

        await message.answer(f'Ваши данные:\n\n'
                             f'Имя: {data.get("name")}\n'
                             f'Возраст: {data.get("age")} лет\n'
                             f'Вес: {data.get("weight")} кг\n'
                             f'Рост: {data.get("height")} см\n'
                             f'Уровень активности: {data.get("activity_level")} минут в день\n'
                             f'Город: {data.get("city")}\n'
                             f'Цель калорий: {calories} ккал (по умолчанию)')
    else:
        await state.update_data(custom_calorie_goal=message.text)
        data = await message.answer(f'Ваши данные:\n\n'
                             f'Имя: {data.get("name")}\n'
                             f'Возраст: {data.get("age")} лет\n'
                             f'Вес: {data.get("weight")} кг\n'
                             f'Рост: {data.get("height")} см\n'
                             f'Уровень активности: {data.get("activity_level")} минут в день\n'
                             f'Город: {data.get("city")}\n'
                             f'Цель калорий: {message.text} ккал (задана вручную)')

    # Возврат в главное меню
    await show_keyboard(data)
    await state.clear() # Завершение состояния
###################################Water##############################################
