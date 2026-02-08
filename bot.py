import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from config import TOKEN
from parser import check_light_status, get_full_schedule_text
from database import init_db, add_user
from scheduler import schedule_checker

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    add_user(message.from_user.id)
    await message.answer("Шалом! Я перевіряю чи доберешся ти додому на ліфті.\n"
                         "Команди:\n/check - статус зараз\n/graph - графік на день")

@dp.message(Command("check"))
async def cmd_check(message: types.Message):
    status_msg, _, _ = check_light_status()
    await message.answer(status_msg)

@dp.message(Command("graph"))
async def cmd_graph(message: types.Message):
    await message.answer(get_full_schedule_text())

async def main():
    init_db()
    asyncio.create_task(schedule_checker(bot))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())