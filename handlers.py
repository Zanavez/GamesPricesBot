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
PAGE_SIZE = 5
current_page = 0
game_price_request = []


@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(text.hello_text_message.format(username=msg.from_user.first_name))


@router.message()
async def message_handler(msg: Message):
    global current_page, game_price_request
    current_page = 0
    async with aiohttp.ClientSession() as client_session:
        game_price_request = await models.fetch(client_session,
                                                f"https://bld-team.tech/prices/api/search?query={msg.text}")
        game_price_request = sorted(game_price_request, key=lambda x: len(x['name']))
        print(game_price_request)
        pagination_list_names = [item['name'] for item in game_price_request]
        print(pagination_list_names)

        # game_choice_keyboard = InlineKeyboardBuilder()

        buttons = []
        for i in range(current_page * PAGE_SIZE, (current_page + 1) * PAGE_SIZE):
            if i < len(game_price_request):
                buttons.append(types.InlineKeyboardButton(
                    text=str(pagination_list_names[i]), callback_data=str(game_price_request[i]['id'])))

        if len(game_price_request) > PAGE_SIZE:
            if current_page > 0:
                buttons.append(types.InlineKeyboardButton(text="⏪", callback_data="prev_page"))
            if (current_page + 1) * PAGE_SIZE < len(game_price_request):
                buttons.append(types.InlineKeyboardButton(text="⏩", callback_data="next_page"))

        game_choice_keyboard = InlineKeyboardBuilder()
        game_choice_keyboard.add(*buttons)
        game_choice_keyboard.adjust(1)

        await msg.answer("<b>🕹️ Выберите нужную для вас игру:</b>", reply_markup=game_choice_keyboard.as_markup())


@router.callback_query()
async def callback_handler(callback_query: types.CallbackQuery):
    global current_page

    global current_page
    if callback_query.data == "prev_page":
        if current_page > 0:
            current_page -= 1
        await update_message(callback_query.message)
    elif callback_query.data == "next_page":
        current_page += 1
        await update_message(callback_query.message)

    elif callback_query.data.startswith("subscribe"):
        await callback_subscribe_handler(callback_query)

    else:
        game_id = callback_query.data
        chat_id = callback_query.from_user.id

        async with (aiohttp.ClientSession() as client_session):
            try:
                prices_user_message = "<b>" + text.games_prices_message + "</b>"
                game_data = await models.get_request(int(game_id))
                print(game_data)
                game_data = game_data[0]
                for market in game_data['markets']:
                    if market['price'] is not None:
                        prices_user_message = "<b>" + prices_user_message.format(
                            game_name=game_data[
                                'name']) + "</b>" + (
                                                  f"\t\t\t\t\t\t🛒<b>Маркетплейс «{market['name']}»: {'{:.2f}'.format(round(market['price'] / 100, 2))}"
                                                  f"{market['currency']}\n</b>")
                    else:
                        prices_user_message = "<b>" + prices_user_message.format(
                            game_name=game_data['name']) + "</b>" + f"\t\t\t\t\t\t🛒 <b>Маркетплейс «{market['name']}»: {'Бесплатно'}\n </b>"

                subscription_on = [
                    [InlineKeyboardButton(text="✉️ Подписаться на уведомления!",
                                          callback_data=f"subscribe:{str(game_id)}")],
                ]

                subscription_button = InlineKeyboardMarkup(inline_keyboard=subscription_on)

                await callback_query.message.answer(prices_user_message, reply_markup=subscription_button)
                await callback_query.answer()

            except aiohttp.ContentTypeError:
                await callback_query.message.answer("❌ <b>Произошла ошибка при получении данных ❌\n"
                                                    "Скорее всего игра недоступна в вашем регионе!</b> 😭")
                await callback_query.answer()


async def update_message(msg: Message):
    global current_page, game_price_request
    pagination_list_names = [item['name'] for item in game_price_request]
    print(pagination_list_names)

    game_choice_keyboard = InlineKeyboardBuilder()

    buttons = []
    for i in range(current_page * PAGE_SIZE, (current_page + 1) * PAGE_SIZE):
        if i < len(game_price_request):
            buttons.append(types.InlineKeyboardButton(
                text=str(pagination_list_names[i]), callback_data=str(game_price_request[i]['id'])))
    # game_choice_keyboard.adjust(1)

    if len(game_price_request) > PAGE_SIZE:
        if current_page > 0:
            buttons.append(types.InlineKeyboardButton(text="⏪", callback_data="prev_page"))
        if (current_page + 1) * PAGE_SIZE < len(game_price_request):
            buttons.append(types.InlineKeyboardButton(text="⏩", callback_data="next_page"))

    game_choice_keyboard = InlineKeyboardBuilder()
    game_choice_keyboard.add(*buttons)
    game_choice_keyboard.adjust(1)

    await msg.edit_text("<b>🕹️ Выберите нужную для вас игру:</b>", reply_markup=game_choice_keyboard.as_markup())


@router.callback_query()
async def callback_subscribe_handler(callback_query: types.CallbackQuery):
    game_id = callback_query.data[10:]

    try:
        subscription_data = await models.post_request(str(callback_query.from_user.id), int(game_id))
        print("-->" + f"{subscription_data}")

        await callback_query.message.answer("<b>Рассылка успешно включена! ✅</b>")
        await callback_query.answer()

        with open('user_ids.txt', 'r') as file:
            if str(callback_query.from_user.id) not in file.read():
                with open('user_ids.txt', 'a') as file_append:
                    file_append.write(str(callback_query.from_user.id) + '\n')
                    asyncio.Task(models.connect_to_server(chat_id=str(callback_query.from_user.id)))

    except aiohttp.ClientError or json.JSONDecodeError as error:
        print(f"Отловлена ошибка: {error}")
        await callback_query.message.answer("<b>Произошла ошибка при включении рассылки! ❌</b>")

    finally:
        await callback_query.answer()

