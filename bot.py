from requests import request
import telebot
from telebot.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from api.setting import CHAT_ID, TOKEN, URL
import httpx

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def start_command(message: Message):
    bot.send_message(
        message.chat.id,
        "Greetings! I can show you exchange rates.\n"
        + "To get the exchange rates press /exchange.\n"
        + "To get info about crypto /crypto.\n"
        + "To get help press /help.",
    )


@bot.message_handler(commands=["help"])
def help_command(message: Message):
    bot.send_message(
        message.chat.id,
        "For now it is simple bot, have are small functions.",
    )


@bot.message_handler(commands=["exchange"])
def exchange_command(message: Message):
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton("USD", callback_data="get-USD"))
    keyboard.row(
        InlineKeyboardButton("EUR", callback_data="get-EUR"),
        InlineKeyboardButton("RUB", callback_data="get-RUB"),
        InlineKeyboardButton("UAH", callback_data="get-UAH"),
    )
    keyboard.row(InlineKeyboardButton("All", callback_data="get-All"))

    bot.send_message(
        message.chat.id, "Click on the currency of choice:", reply_markup=keyboard
    )


@bot.message_handler(commands=["crypto"])
def crypto_command(message: Message):
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton("BTC", callback_data="crypto-BTC"))
    keyboard.row(
        InlineKeyboardButton("NEAR", callback_data="crypto-NEAR"),
        InlineKeyboardButton("SOLANA", callback_data="crypto-SOL"),
    )
    keyboard.row(InlineKeyboardButton("ALL", callback_data="crypto-ALL"))

    bot.send_message(
        message.chat.id, "Click on the currency of choice:", reply_markup=keyboard
    )


@bot.callback_query_handler(func=lambda call: True)
def iq_callback(query: CallbackQuery) -> None:
    data: str = query.data
    if data.startswith("get-"):
        exc = query.data[4:]
        ret = get_exchange()
        if exc == 'All':
            bot.send_message(query.message.chat.id, f"{exc}: {ret}")
        else:
            bot.send_message(query.message.chat.id, f"{exc}: {ret.get(exc)}")
    elif data.startswith('crypto-'):
        coin = query.data[7:]
        ret = get_crypto(coin)
        bot.send_message(query.message.chat.id, f"{coin}: {ret}")


def get_crypto(coin: str) -> dict:
    """
    Get information about coins rates from "https://min-api.cryptocompare.com API.
    """
    coins = ['BTC', 'NEAR', 'SOL']
    if coin == 'ALL':
        API_URL = f"https://min-api.cryptocompare.com/data/pricemulti?fsyms={','.join(coins)}&tsyms=USD,EUR"
    else:
        API_URL = f"https://min-api.cryptocompare.com/data/price?fsym={coin}&tsyms=USD,EUR"
    res = request("GET", API_URL)
    res_json = res.json()
    print(res.json())
    print(API_URL)
    return res_json

def get_exchange() -> dict:
    """
    Get information about exchange rates from nbrb.by API.
    """
    ret_json = {}
    API_URL = "https://www.nbrb.by/api/exrates/rates?periodicity=0"
    res = request("GET", API_URL)
    for i in res.json():
        ret_json.update({i.get("Cur_Abbreviation"): i.get("Cur_OfficialRate")})
    return ret_json


bot.polling(none_stop=True)
