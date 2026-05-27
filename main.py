from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models.bubbletea import BubbleTea, BubbleTeaCreate
from routes.bubbletea import router as bubbletea_router
from routes.pedido import router as pedido_router
from utils.db_connection import get_connection

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def say_hello():
    return {"message": "Hello, World!"}

app.include_router(bubbletea_router)
app.include_router(pedido_router)