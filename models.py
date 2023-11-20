import aiohttp
import json


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()


async def get_request(game_id):
    async with aiohttp.ClientSession() as session:
        response = await session.get(url=f"https://bld-team.tech/prices/api/search/{game_id}")
        text_response = await response.text()
        return json.loads(text_response)


async def post_request(chat_id, game_id):
    async with aiohttp.ClientSession() as session:
        response = await session.post(url="https://bld-team.tech/prices/api/subscribe",
                                      json={
                                          "gameId": game_id,
                                          "chatId": chat_id
                                      },
                                      headers={"Content-Type": "application/json"})
        text_response = await response.text()
        print(text_response)
        return json.loads(text_response)