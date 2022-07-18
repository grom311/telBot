# app.py
import random

import httpx
import telebot
from fastapi import APIRouter, Request
from telebot import types

from .setting import CHAT_ID, TOKEN, URL

router = APIRouter()
bot = telebot.TeleBot(TOKEN)


@router.api_route("/setwebhook", methods=["GET", "POST"])
async def set_webhook():
    # we use the bot object to link the bot to our app which live
    # in the link provided by URL
    # s = bot.set_webhook('{URL}{HOOK}'.format(URL=URL, HOOK=token))

    s = bot.set_webhook(f"{URL}/hook")
    # something to let us know things work
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"

@router.api_route("/delete_webhook", methods=["DELETE"])
async def delet_webhook():
    # we use the bot object to link the bot to our app which live
    # in the link provided by URL
    # s = bot.set_webhook('{URL}{HOOK}'.format(URL=URL, HOOK=token))

    s = bot.delete_webhook(f"{URL}/hook")
    # something to let us know things work
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"

first = [
    "Сегодня — идеальный день для новых начинаний.",
    "Оптимальный день для того, чтобы решиться на смелый поступок!",
    "Будьте осторожны, сегодня звёзды могут повлиять на ваше финансовое состояние.",
    "Лучшее время для того, чтобы начать новые отношения или разобраться со старыми.",
    "Плодотворный день для того, чтобы разобраться с накопившимися делами.",
]
second = [
    "Но помните, что даже в этом случае нужно не забывать про",
    "Если поедете за город, заранее подумайте про",
    "Те, кто сегодня нацелен выполнить множество дел, должны помнить про",
    "Если у вас упадок сил, обратите внимание на",
    "Помните, что мысли материальны, а значит вам в течение дня нужно постоянно думать про",
]
second_add = [
    "отношения с друзьями и близкими.",
    "работу и деловые вопросы, которые могут так некстати помешать планам.",
    "себя и своё здоровье, иначе к вечеру возможен полный раздрай.",
    "бытовые вопросы — особенно те, которые вы не доделали вчера.",
    "отдых, чтобы не превратить себя в загнанную лошадь в конце месяца.",
]
third = [
    "Злые языки могут говорить вам обратное, но сегодня их слушать не нужно.",
    "Знайте, что успех благоволит только настойчивым, поэтому посвятите этот день воспитанию духа.",
    "Даже если вы не сможете уменьшить влияние ретроградного Меркурия, то хотя бы доведите дела до конца.",
    "Не нужно бояться одиноких встреч — сегодня то самое время, когда они значат многое.",
    "Если встретите незнакомца на пути — проявите участие, и тогда эта встреча посулит вам приятные хлопоты.",
]


@router.post("/hook")
async def req_webhook(req: Request):
    """
    Receive the Webhook and process the Webhook Payload to get relevant data
    Refer https://developer.github.com/webhooks/event-payloads for all GitHub Webhook Events and Payloads
    Work for local API with ngrok
    """
    body = await req.json()
    print(body)
    event = req.headers.get("X-Github-Event")
    print(f"event: {event}")
    if event == "star":  # check if the event is a star
        nos_stars = body["repository"]["stargazers_count"]
        starrer_username = body["sender"]["login"]
        repo_url = body["repository"]["html_url"]
        repo_name = body["repository"]["name"]
        message = f"{starrer_username} has starred the [{repo_name}]({repo_url}). \n\n The Total Stars are {nos_stars}"
        await send_tg_message(message)
    elif body.get("callback_query") and body["callback_query"]["data"] == "oven":
        await send_tg_message("api to oven")
    elif body.get("callback_query") and body["callback_query"]["data"] == "zodiac":
        # Формируем гороскоп
        msg = (
            random.choice(first)
            + " "
            + random.choice(second)
            + " "
            + random.choice(second_add)
            + " "
            + random.choice(third)
        )
        # Отправляем текст в Телеграм
        bot.send_message(CHAT_ID, msg)
        await send_tg_message("zodiac any ")
    elif body.get("callback_query") and body["callback_query"]["data"] == "USD":
        ret = await get_exchange()
        await send_tg_message(f"USD: {ret.get('USD')}")
    elif body.get("callback_query") and body["callback_query"]["data"] == "EUR":
        ret = await get_exchange()
        await send_tg_message(f"EUR: {ret.get('EUR')}")
    elif body.get("callback_query") and body["callback_query"]["data"] == "All":
        ret = await get_exchange()
        await send_tg_message(ret)
    elif body.get("message") and body["message"]["text"] == "exchange":
        # bot.send_message(CHAT_ID, "I am finding exchange!")
        keyboard = types.InlineKeyboardMarkup()
        exchange = types.InlineKeyboardButton(text="USD", callback_data="USD")
        keyboard.add(exchange)
        exchange = types.InlineKeyboardButton(text="EUR", callback_data="EUR")
        keyboard.add(exchange)
        exchange = types.InlineKeyboardButton(text="All", callback_data="All")
        keyboard.add(exchange)
        bot.send_message(CHAT_ID, text="Choose currency", reply_markup=keyboard)

    elif body.get("message") and body["message"]["text"] == "hi":
        bot.send_message(CHAT_ID, "Hello, now I will tell you the horoscope for today.")
        # Готовим кнопки
        keyboard = types.InlineKeyboardMarkup()
        # По очереди готовим текст и обработчик для каждого знака зодиака
        key_zodiac = types.InlineKeyboardButton(text="Овен", callback_data="oven")
        # И добавляем кнопку на экран
        keyboard.add(key_zodiac)
        key_zodiac = types.InlineKeyboardButton(text="Телец", callback_data="zodiac")
        keyboard.add(key_zodiac)
        key_zodiac = types.InlineKeyboardButton(text="Близнецы", callback_data="zodiac")
        keyboard.add(key_zodiac)
        key_zodiac = types.InlineKeyboardButton(text="Рак", callback_data="zodiac")
        keyboard.add(key_zodiac)
        key_zodiac = types.InlineKeyboardButton(text="Лев", callback_data="zodiac")
        keyboard.add(key_zodiac)
        key_zodiac = types.InlineKeyboardButton(text="Дева", callback_data="zodiac")
        keyboard.add(key_zodiac)
        key_zodiac = types.InlineKeyboardButton(text="Весы", callback_data="zodiac")
        keyboard.add(key_zodiac)
        key_zodiac = types.InlineKeyboardButton(text="Скорпион", callback_data="zodiac")
        keyboard.add(key_zodiac)
        key_zodiac = types.InlineKeyboardButton(text="Стрелец", callback_data="zodiac")
        keyboard.add(key_zodiac)
        key_zodiac = types.InlineKeyboardButton(text="Козерог", callback_data="zodiac")
        keyboard.add(key_zodiac)
        key_zodiac = types.InlineKeyboardButton(text="Водолей", callback_data="zodiac")
        keyboard.add(key_zodiac)
        key_zodiac = types.InlineKeyboardButton(text="Рыбы", callback_data="zodiac")
        keyboard.add(key_zodiac)
        bot.send_message(CHAT_ID, text="Choose your zodiac sign", reply_markup=keyboard)
    elif body.get("message") and body["message"]["text"] == "stop":
        await send_tg_message("stop Bot!")
    elif body.get("message") and body["message"]["text"] == "/help":
        await send_tg_message(f"Exists commands:\n hi, stop, exchange")
    else:
        await send_tg_message("I do not know who you are.")


async def send_tg_message(message: str):
    """
    Sends the Message to telegram with the Telegram BOT API.
    """
    # print(message)
    tg_msg = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    API_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    async with httpx.AsyncClient() as client:
        res = await client.post(API_URL, json=tg_msg)
        # print(f"res : {res.json()}")


async def get_exchange():
    """
    Get information about exchange rates from nbrb.by API.
    """
    ret_json = {}
    API_URL = f"https://www.nbrb.by/api/exrates/rates?periodicity=0"
    async with httpx.AsyncClient() as client:
        res = await client.get(API_URL)
        for i in res.json():
            ret_json.update({i.get("Cur_Abbreviation"): i.get("Cur_OfficialRate")})
    return ret_json
