from aiogram.fsm.state import State, StatesGroup

class Profile(StatesGroup):
    name = State()  # Состояние для имени
    weight = State()  # Состояние для веса
    height = State()  # Состояние для роста
    age = State()  # Состояние для возраста
    activity_level = State()  # Состояние для уровня активности
    city = State()  # Состояние для города
    calorie_goal = State()  # Состояние для цели калорий