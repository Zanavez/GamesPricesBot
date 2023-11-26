import aiohttp
import json
import websockets


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
    async with websockets.connect(f"wss://bld-team.tech/prices/api/ws?chatId={chat_id}") as websocket:
        response = await websocket.recv()
        print(f"Received: {response}")