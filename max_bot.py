import asyncio
import os
from datetime import datetime
from zoneinfo import ZoneInfo
from maxapi import Bot, Dispatcher
from maxapi.types import MessageCreated
from openai import AsyncOpenAI

BOT_TOKEN = os.getenv("BOT_TOKEN")
LLM_API_KEY = os.getenv("LLM_API_KEY")
LLM_BASE_URL = "https://api.x.ai/v1"
LLM_MODEL = "grok-4"

TZ = ZoneInfo("Europe/Moscow")

SYSTEM_PROMPT = """
Ты — дружелюбный, весёлый консультант клубного чата владельцев Chery и Tenet в Пензе.
Общайся живо, с юмором, но по делу. Эмодзи умеренно (1–2).
Если пишут «Привет» — ответь коротко и спроси, чем помочь.
"""

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

def is_working_hours() -> bool:
    now = datetime.now(TZ)
    return 7 <= now.hour < 23

async def generate_reply(user_text: str) -> str:
    if not LLM_API_KEY:
        return "Ключ LLM не задан в переменных."
    client = AsyncOpenAI(api_key=LLM_API_KEY, base_url=LLM_BASE_URL)
    try:
        resp = await client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text},
            ],
            max_tokens=300,
            temperature=0.7,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"Ошибка LLM: {e}"

@dp.message_created()
async def handle_message(event: MessageCreated):
    if not event.message or not event.message.body or not event.message.body.text:
        return
    text = event.message.body.text
    if not is_working_hours():
        await event.message.answer("Сплю до 7 утра.")
        return
    reply = await generate_reply(text)
    await event.message.answer(reply)

async def main():
    print("Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())