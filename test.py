from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


api = '7759754578:AAHgeVXP3zhIOxjgJZ9uL6Yygjm7vHdS80E'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())
kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Рассчитать")],
        [KeyboardButton(text="Информация")]
    ], resize_keyboard=True
)
inl_kb = InlineKeyboardMarkup()
calor_but = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
formul_but = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
inl_kb.add(calor_but)
inl_kb.add(formul_but)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=inl_kb)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer(f'Упрощенный вариант формулы Миффлина-Сан Жеора:\n'
                              f'Для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5\n'
                              f'для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161')
    await call.answer()


@dp.callback_query_handler(text="calories")
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()
    await call.answer()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    if int(message) >  199:
        await message.answer('Не пизди')
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    calories_calk_male = 10 * int(data["weight"]) + 6.25 * int(data["growth"]) - 5 * int(data["age"]) + 5
    user_id = message.from_user.id
    with open('module_13_2', 'a') as file:
        file.write(f'{user_id}: {data["weight"]}, {data["age"]}, {data["growth"]}\n')
    file.close()
    await message.answer(
        f'Ваша норма каллорий для поддержания нормального веса:\nесли вы мужчина: {calories_calk_male}\nесли вы женщина: {calories_calk_male - 166}')
    await state.finish()


@dp.message_handler(commands=['start'])
async def start(message):
    print('Привет! Я бот помогающий твоему здоровью.')
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)


@dp.message_handler()
async def all_message(message):
    print('Введите команду /start, чтобы начать общение.')
    await message.answer("Введите команду /start, чтобы начать общение.")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
