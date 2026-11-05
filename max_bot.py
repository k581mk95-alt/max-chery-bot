import asyncio
import os
from maxapi import Bot, Dispatcher
from maxapi.types import MessageCreated

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(BOT_TOKEN)
dp = Dispatcher()

@dp.message_created()
async def handle_message(event: MessageCreated):
    if event.message and event.message.body and event.message.body.text:
        await event.message.answer(f"Получил: {event.message.body.text}")

async def main():
    print("Эхо-бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())