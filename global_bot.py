import asyncio, logging
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, types, filters
import data_token
import config
logging.basicConfig(level=logging.INFO)
bot = Bot(token=data_token.TOKEN)
dp = Dispatcher(storage=MemoryStorage())


@dp.message(filters.Command('start'))
async def start_command(message: types.Message):
    await message.answer('Привет, я бот-магазин, через меня ты сможешь совершать покупки одежды и прочего. '
                         'Чтобы увидеть мой функционал достаточно ввести команду /menu')


@dp.message(filters.Command('menu'))
async def fuctions_command(message: types.Message):
    await message.answer('Выбери одну из кнопок:', reply_markup=config.keyboard1)


async def main():
    dp.include_routers(config.router)
    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())