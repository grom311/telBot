# telBot
telegram bot

1. For local work:  
  uvicorn main:app --reload --port 9000  
  ngrok http 9000  
  URL="https://b7dd-178-127-235-232.ngrok.io"  
2. Create webhook and use it in variable URL

# Api
http://127.0.0.1:9000/docs  
First set the webhook on the /setwebhook endpoint  

Env Variables:  
TOKEN = ""  
CHAT_ID = ""  
URL = ""  

# telBot
bot.py  
simple bot without webhook
