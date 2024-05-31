import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = '7346873674:AAHAJgAh1ZBbogGUzBnwhqJFJ6WI6hEtV8I'

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher()


# Состояния для FSM
class CalcStates(StatesGroup):
    waiting_for_cost = State()


# Стартовое сообщение и кнопка
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Привет!\n\nЯ бот-калькулятор подписчиков для трафферов.", reply_markup=user_menu)


# Обработчик нажатия кнопки "Подсчет подписчика"
@dp.message(lambda message: message.text == 'Подсчет за подписчика 🧮')
async def ask_for_cost(message: types.Message, state: FSMContext):

    await bot.send_chat_action(message.from_user.id, action="typing")
    await bot.send_message(message.from_user.id, "Введите стоимость за одного подписчика:", reply_markup=cancel_inline())
    await state.set_state(CalcStates.waiting_for_cost)


# Обработчик ввода стоимости за подписчика
@dp.message(CalcStates.waiting_for_cost)
async def calculate_costs(message: types.Message, state: FSMContext):
    try:
        cost = float(message.text)
        counts = [10, 100, 500, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 10000, 20000, 30000, 40000, 50000]
        response = "Стоимость за подписчиков:\n\n"
        for count in counts:
            response += f"{count} подписчиков: {cost * count}$.\n"
        await message.answer(response, reply_markup=user_menu)
    except ValueError:
        await message.answer("Пожалуйста, введите правильную стоимость (число).")
    finally:
        await state.clear()


# Обработчик нажатия кнопки "Отменить"
@dp.callback_query(lambda c: c.data == 'cancel')
async def cancel(callback_query: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback_query.answer(text="", show_alert=True)
    await callback_query.message.delete()
    await callback_query.message.answer("Операция отменена.", reply_markup=user_menu)


# inline
def cancel_inline():
    inline_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Отменить", callback_data="cancel")]
        ]
    )
    return inline_keyboard


user_menu = types.ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [types.KeyboardButton(text="Подсчет за подписчика 🧮")],
    ]
)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
