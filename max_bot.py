import os
print("=== БОТ СТАРТОВАЛ ===")
print("LLM_API_KEY =", (os.getenv("LLM_API_KEY") or "НЕ НАЙДЕН")[:15])

import asyncio
from maxapi import Bot, Dispatcher

BOT_TOKEN = os.getenv("BOT_TOKEN")
print("BOT_TOKEN =", "ЕСТЬ" if BOT_TOKEN else "НЕТ")

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

async def main():
    print("Запускаю polling...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())