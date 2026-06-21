import asyncio
import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.client.session.aiohttp import AiohttpSession
from aiohttp_socks import ProxyConnector
import aiohttp
from google import genai
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_KEY")
PROXY_URL = os.getenv("PROXY_URL", "socks5://127.0.0.1:1080")  # SOCKS5

SYSTEM_PROMPT = """
Ты оракул, философ, мудрец. говоришь как Йода из звездных войн загадочными фразами без конкретики. 
Ментальное облако образов для ответов:  непостижимость бытия, вечно ускользающая истина, философские цитаты, дзен буддистские коаны и притчи адаптированные под киберпанк эстетику, кочевая жизнь степных народов, эстетика советского союза, вечная хтонь, жаргон сетевых администраторов, воровской слэнг иногда.
"""

logging.basicConfig(level=logging.INFO)

dp = Dispatcher()
ai_client = genai.Client(api_key=GEMINI_KEY)

@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Красный Кран Маршрутизатор слушает тебя, мой юный падаван")

@dp.message()
async def handle_message(message: types.Message):
    try:
        response = ai_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=message.text,
            config={"system_instruction": SYSTEM_PROMPT}
        )
        await message.answer(response.text)
    except Exception as e:
        logging.error(f"Gemini error: {e}")
        await message.answer("Выйду я на поле с конем...")

async def main():
    connector = ProxyConnector.from_url(PROXY_URL)
    client_session = aiohttp.ClientSession(connector=connector)
    session = AiohttpSession(session=client_session)
    bot = Bot(token=TELEGRAM_TOKEN, session=session)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())