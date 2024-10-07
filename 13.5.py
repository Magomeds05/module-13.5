from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext
import asyncio

api = "8197570567:AAF2r-nMMyE_nqJ4Ll3dAHgXvzRn5kNVegw"
bot = Bot(token= api)
disp = Dispatcher(bot, storage=MemoryStorage())

key = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Информация')
button2 = KeyboardButton(text='Рассчитать')
key.add(button)
key.add(button2)


@disp.message_handler(commands=['start'])
async def start(message):
    print('Привет! Я бот помогающий твоему здоровью.')
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=key)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@disp.message_handler(text = ['Рассчитать'])
async def set_age(message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()

@disp.message_handler(state= UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@disp.message_handler(state= UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@disp.message_handler(state= UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    w = data['weight']
    g = data['growth']
    a = data['age']
    await message.answer(f"Ваша норма калорий в день: {(10 * int(w)) + (6.25 * int(g)) - (5 * int(a)) + 5}")

@disp.message_handler()
async def all_massages(message):
    print('Введите команду /start, чтобы начать общение.')
    await message.answer('Введите команду /start, чтобы начать общение.')


#10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5;

if __name__ == "__main__":
    executor.start_polling(disp, skip_updates=True)