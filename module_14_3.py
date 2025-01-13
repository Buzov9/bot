from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import time


api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())
kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Рассчитать"), KeyboardButton(text="Информация")],
        [KeyboardButton(text="Купить")]
    ], resize_keyboard=True
)
inl_kb = InlineKeyboardMarkup()
calor_but = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
formul_but = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
inl_kb.add(calor_but)
inl_kb.add(formul_but)

products_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Product1', callback_data="product_buying"),
         InlineKeyboardButton(text='Product2', callback_data="product_buying"),
         InlineKeyboardButton(text='Product3', callback_data="product_buying"),
         InlineKeyboardButton(text='Product4', callback_data="product_buying")
         ]
    ]
)



class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(text= 'Купить')
async def get_buying_list(message):
    with open('1.jpg', 'rb') as img:
        await message.answer_photo(img, 'Название: Product 1\nОписание: Описание 1\nЦена: 100', )
    time.sleep(1)
    with open('2.jpg', 'rb') as img:
        await message.answer_photo(img, 'Название: Product 2\nОписание: Описание 2\nЦена: 200')
    time.sleep(1)
    with open('3.jpg', 'rb') as img:
        await message.answer_photo(img, 'Название: Product 3\nОписание: Описание 3\nЦена: 300')
    time.sleep(1)
    with open('4.jpg', 'rb') as img:
        await message.answer_photo(img, 'Название: Product 4\nОписание: Описание 4\nЦена: 400')
    await message.answer("Выберите продукт для покупки:", reply_markup=products_kb)


@dp.callback_query_handler(text="product_buying")
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()
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
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    calories_calk_male = 10 * int(data["weight"]) + 6.25 * int(data["growth"]) - 5 * int(data["age"]) + 5
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
