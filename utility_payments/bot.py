import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession

session = AiohttpSession(proxy="http://127.0.0.1:8000")  # замени порт на свой
bot = Bot(token="9255717121:AAFWTJgx4MYW686FbeWnwf8rj26Ih-Xjw8Q", session=session)
dp = Dispatcher()

# Токен лучше брать из переменной окружения, но для теста можно вставить строкой
BOT_TOKEN = os.getenv("BOT_TOKEN", "9255717121:AAFWTJgx4MYW686FbeWnwf8rj26Ih-Xjw8Q")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Обработчик команды /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        f"Привет! Я бот для учёта коммуналки.\n"
        f"Твой chat_id: {message.chat.id}\n"
        f"Отправь мне показания в формате: /вода 12.5 8.3"
    )

# Обработчик ввода показаний (пример)
@dp.message(Command("вода"))
async def cmd_water(message: types.Message):
    # message.text будет содержать: /вода 12.5 8.3
    args = message.text.split()[1:] # отрезаем саму команду
    if len(args) != 2:
        await message.answer("Ошибка. Пиши так: /вода 12.5 8.3 (холодная и горячая)")
        return
    
    cold, hot = args
    # ЗДЕСЬ ПОЗЖЕ БУДЕТ КОД, КОТОРЫЙ ПИШЕТ ДАННЫЕ В БАЗУ DJANGO
    await message.answer(f"Принято! Холодная: {cold}, Горячая: {hot}. (Пока не сохранил, это тест)")

async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())