from requests import request
import telebot
from telebot import types
from api.setting import CHAT_ID, TOKEN, URL
import httpx

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def start_command(message):
    bot.send_message(
        message.chat.id,
        "Greetings! I can show you exchange rates.\n"
        + "To get the exchange rates press /exchange.\n"
        + "To get help press /help.",
    )


@bot.message_handler(commands=["exchange"])
def exchange_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(telebot.types.InlineKeyboardButton("USD", callback_data="get-USD"))
    keyboard.row(
        telebot.types.InlineKeyboardButton("EUR", callback_data="get-EUR"),
        telebot.types.InlineKeyboardButton("RUB", callback_data="get-RUB"),
        telebot.types.InlineKeyboardButton("UAH", callback_data="get-UAH"),
    )
    keyboard.row(telebot.types.InlineKeyboardButton("All", callback_data="get-All"))

    bot.send_message(
        message.chat.id, "Click on the currency of choice:", reply_markup=keyboard
    )


@bot.callback_query_handler(func=lambda call: True)
def iq_callback(query):
    data = query.data
    if data.startswith("get-"):
        exc = query.data[4:]
        # print(exc)
        ret = get_exchange()
        if exc == 'All':
            bot.send_message(query.message.chat.id, f"{exc}: {ret}")
        else:
            bot.send_message(query.message.chat.id, f"{exc}: {ret.get(exc)}")


def get_exchange():
    """
    Get information about exchange rates from nbrb.by API.
    """
    ret_json = {}
    API_URL = f"https://www.nbrb.by/api/exrates/rates?periodicity=0"
    res = request("GET", API_URL)
    for i in res.json():
        ret_json.update({i.get("Cur_Abbreviation"): i.get("Cur_OfficialRate")})
    return ret_json


bot.polling(none_stop=True)
