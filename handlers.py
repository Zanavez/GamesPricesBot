import asyncio
import json
from aiogram import types, F, Router
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
import aiohttp
import text
import models
from aiogram.utils.keyboard import InlineKeyboardBuilder
router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(text.hello_text_message.format(username=msg.from_user.first_name))


@router.message()
async def message_handler(msg: Message):
    async with aiohttp.ClientSession() as client_session:
        game_price_request = await models.fetch(client_session,
                                                f"https://bld-team.tech/prices/api/search?query={msg.text}")
        game_price_request = sorted(game_price_request, key=lambda x: len(x['name']))
        print(game_price_request)

        game_choice_keyboard = InlineKeyboardBuilder()
        for game in game_price_request:
            game_choice_keyboard.add(types.InlineKeyboardButton(
                text=str(game['name']), callback_data=str(game['id'])))
        game_choice_keyboard.adjust(1)
        await msg.answer("🕹️ Выберите нужную для вас игру:", reply_markup=game_choice_keyboard.as_markup())


@router.callback_query()
async def callback_handler(callback_query: types.CallbackQuery):
    if callback_query.data.startswith("subscribe"):
        await callback_subscribe_handler(callback_query)
    else:
        game_id = callback_query.data
        chat_id = callback_query.from_user.id

        async with (aiohttp.ClientSession() as client_session):
            try:
                prices_user_message = "" + text.games_prices_message
                game_data = await models.get_request(int(game_id))
                print(game_data)
                game_data = game_data[0]
                for market in game_data['markets']:
                    if market['price'] is not None:
                        prices_user_message = prices_user_message.format(
                            game_name=game_data[
                                'name']) + (f"🕹️ {market['name']}: {'{:.2f}'.format(round(market['price'] / 100, 2))}"
                                            f"{market['currency']}\n")
                    else:
                        prices_user_message = prices_user_message.format(
                            game_name=game_data['name']) + f"{market['name']}: {'Бесплатно'}\n"

                subscription_on = [
                    [InlineKeyboardButton(text="✉️ Подписаться на уведомления!",
                                          callback_data=f"subscribe:{str(game_id)}")],
                ]

                subscription_button = InlineKeyboardMarkup(inline_keyboard=subscription_on)

                await callback_query.message.answer(prices_user_message, reply_markup=subscription_button)
                await callback_query.answer()

            except aiohttp.ContentTypeError:
                await callback_query.message.answer("❌ Произошла ошибка при получении данных ❌\n"
                                                    "Скорее всего игра недоступна в вашем регионе! 😭")


@router.callback_query()
async def callback_subscribe_handler(callback_query: types.CallbackQuery):
    game_id = callback_query.data[10:]

    try:
        subscription_data = await models.post_request(str(callback_query.from_user.id), int(game_id))
        await callback_query.message.answer("Рассылка успешно включена! ✅")
        await callback_query.answer()
    except aiohttp.ClientError or json.JSONDecodeError as error:
        print(f"An error occurred: {error}")
        await callback_query.message.answer("Произошла ошибка при включении рассылки! ❌")
    finally:
        await callback_query.answer()
