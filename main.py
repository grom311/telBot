# main.py

from fastapi import FastAPI
from api.app import router

app = FastAPI()
app.include_router(router)


# uvicorn main:app --reload --port 9000
# ngrok http 9000