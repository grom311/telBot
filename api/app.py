# main.py
from fastapi import Request
from fastapi import APIRouter
import httpx
import telebot


router = APIRouter()
# https://api.telegram.org/bot5449976483:AAH6_qytNGxw9CrXJ_SoShpgAo-80emNFIM/getUpdates
TOKEN = "5449976483:AAH6_qytNGxw9CrXJ_SoShpgAo-80emNFIM"  # Telegram Bot API Key
CHAT_ID = '800601219'  # Telegram Chat ID
URL = 'https://b7dd-178-127-235-232.ngrok.io'
bot = telebot.TeleBot(TOKEN)


@router.api_route('/setwebhook', methods=['GET', 'POST'])
async def set_webhook():
    # we use the bot object to link the bot to our app which live
    # in the link provided by URL
    # s = bot.set_webhook('{URL}{HOOK}'.format(URL=URL, HOOK=token))

    s = bot.set_webhook('{URL}/hook'.format(URL=URL))
    # something to let us know things work
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"

async def sendTgMessage(message: str):
    """
    Sends the Message to telegram with the Telegram BOT API
    """
    print(message)
    tg_msg = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    API_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    print(f"API url: {API_URL}")
    async with httpx.AsyncClient() as client:
        res = await client.post(API_URL, json=tg_msg)
        print(f"res : {res.json()}")

@router.post("/hook")
async def recWebHook(req: Request):
    """
    Receive the Webhook and process the Webhook Payload to get relevant data
    Refer https://developer.github.com/webhooks/event-payloads for all GitHub Webhook Events and Payloads
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
        await sendTgMessage(message)
    elif event == "pull_request":  # check if event is a pull request
        pr_number = body["number"]
        if body["pull_request"]["merged"] == True:
            pr_action = "merged"
        pr_action = body["action"]
        pr_title = body["pull_request"]["title"]
        pr_desc = body["pull_request"]["body"]
        pr_login = body["sender"]["login"]
        pr_login_url = body["sender"]["html_url"]
        pr_url = body["pull_request"]["html_url"]
        message = f"Pull Request([{pr_number}]({pr_url})) {pr_action} by [{pr_login}]({pr_login_url}).\n\n Title: {pr_title} \n\n Description: {pr_desc}"
        await sendTgMessage(message)
    elif event == "стоп":
        await sendTgMessage('ок стоп')
    else:
        await sendTgMessage('я не знаю кто ты')
