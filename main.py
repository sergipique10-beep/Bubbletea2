from fastapi import FastAPI
from typing import TypedDict

app = FastAPI()

class BubbleTea(TypedDict):
    id: int
    name: str
    temperature: str
    price: float
    active: bool

bubble_teas: list[BubbleTea] = [
    {"id": 1, "name": "Té de Burbuja Clásico", "temperature": "hot", "price": 3.99, "active": True},
    {"id": 2, "name": "Té de Burbuja de Fresa", "temperature": "cold", "price": 4.49, "active": True},
    {"id": 3, "name": "Té de Burbuja de Mango", "temperature": "cold", "price": 4.99, "active": True},
    {"id": 4, "name": "Té de Burbuja de Lichi", "temperature": "cold", "price": 5.49, "active": True},
    {"id": 5, "name": "Té de Burbuja de Chocolate", "temperature": "hot", "price": 5.99, "active": False},
]

@app.get("/")
def say_hello():
    return {"message": "Hello, World!"}

@app.get("/bubbleteas")
def get_bubble_teas() -> list[BubbleTea]:
    return filter_out_inactive_bubble_teas()    

def filter_out_inactive_bubble_teas() -> list[BubbleTea]:
    return [bubble_tea for bubble_tea in bubble_teas if bubble_tea["active"]]