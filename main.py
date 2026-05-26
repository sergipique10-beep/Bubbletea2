from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from models.bubbletea import BubbleTea, BubbleTeaCreate
from routes.bubbletea import router as bubbletea_router
from utils.db_connection import get_connection

app = FastAPI()

@app.get("/")
def say_hello():
    return {"message": "Hello, World!"}

app.include_router(bubbletea_router)