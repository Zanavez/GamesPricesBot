import asyncio

import aiohttp
import json
import websockets
import ssl
from bot import bot
from aiogram.enums import ParseMode

ssl_context = ssl.SSLContext()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()


async def get_request(game_id):
    async with aiohttp.ClientSession() as session:
        response = await session.get(url=f"https://bld-team.tech/prices/api/search/{game_id}")
        text_response = await response.json()
        return text_response


async def post_request(chat_id, game_id):
    async with aiohttp.ClientSession() as session:
        response = await session.post(url="https://bld-team.tech/prices/api/subscribe",
                                      json={
                                          "gameId": game_id,
                                          "chatId": chat_id
                                      },
                                      headers={"Content-Type": "application/json"})
        text_response = await response.json()
        print(text_response)
        return text_response


async def connect_to_server(chat_id):
    print(f"run {chat_id}")
    async with websockets.connect(f"wss://bld-team.tech/prices/api/ws?chatId={chat_id}", ssl=ssl_context) as websocket:
        task = asyncio.create_task(connect(chat_id, websocket))
        await task


async def connect(chat_id, websocket):
    while True:
        response = await websocket.recv()
        try:
            games = json.loads(response)
            await reply_with_websockets(chat_id, games)
        except Exception as e:
            print(f"Received: {response}, Error: {e}")


async def reply_with_websockets(chat_id, data):
    update_message_text = "<b>🕰️ Обновлённый список ваших товаров:</b> \n\n"
    for game in data:
        update_message_text += f"<b><u>{game['name']}</u></b>\n"
        for market in game['markets']:
            update_message_text += f"<b>\t\t\t\t\t\t🛒\tМаркетплейс «{market['name']}», Цена: <a href=\"{market['link']}\">{'{:.2f}'.format(round(market['price'] / 100, 2))} {market['currency']}</a></b>\n"
    asyncio.run(await bot.send_message(chat_id, update_message_text, parse_mode=ParseMode.HTML, disable_web_page_preview=True))
