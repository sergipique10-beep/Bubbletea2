from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()


def get_connection():
    return pymysql.connect(
        charset="utf8mb4",
        connect_timeout=5,
        cursorclass=pymysql.cursors.DictCursor,
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"],
        port=int(os.environ["DB_PORT"]),
        read_timeout=5,
    )

class BubbleTeaCreate(BaseModel):
    name: str
    temperature: str
    price: float
    active: bool

class BubbleTea(BubbleTeaCreate):
    id: int

productos: list[BubbleTea] = [
    BubbleTea(id=1, name="Té de Burbuja Clásico",     temperature="hot",  price=3.99, active=True),
    BubbleTea(id=2, name="Té de Burbuja de Fresa",    temperature="cold", price=4.49, active=True),
    BubbleTea(id=3, name="Té de Burbuja de Mango",    temperature="cold", price=4.99, active=True),
    BubbleTea(id=4, name="Té de Burbuja de Lichi",    temperature="cold", price=5.49, active=True),
    BubbleTea(id=5, name="Té de Burbuja de Chocolate",temperature="hot",  price=5.99, active=False),
]

@app.get("/")
def say_hello():
    return {"message": "Hello, World!"}

@app.get("/bubbleteas")
def get_productos() -> list[BubbleTea]:
    return filter_out_inactive_productos()   

@app.get("/bubbleteasfromaiven/{id}")
def get_bubble_tea_from_aiven(id: int) -> BubbleTea:
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM bubble_teas WHERE id = %s AND active = 1", (id,))
            result = cursor.fetchone()
            if not result:
                raise HTTPException(status_code=404, detail="Bubble tea not found")
            return BubbleTea(**result)
    finally:
        connection.close()

@app.get("/bubbleteasfromaiven")
def get_productos_from_aiven() -> list[BubbleTea]:
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM bubble_teas WHERE active = 1")
            result = cursor.fetchall()
            return [BubbleTea(**row) for row in result]
    finally:
        connection.close()

@app.post("/bubbleteasfromaiven")
def add_bubble_tea_to_aiven(bubble_tea: BubbleTeaCreate) -> BubbleTea:
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO bubble_teas (name, temperature, price, active) VALUES (%s, %s, %s, %s)",
                (bubble_tea.name, bubble_tea.temperature, bubble_tea.price, bubble_tea.active),
            )
            connection.commit()
            return BubbleTea(id=cursor.lastrowid, **bubble_tea.model_dump())
    finally:
        connection.close()

@app.delete("/bubbleteasfromaiven/{id}")
def soft_delete_bubble_tea_from_aiven(id: int):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("UPDATE bubble_teas SET active = 0 WHERE id = %s", (id,))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Bubble tea not found")
            connection.commit()
            return {"message": "Bubble tea soft-deleted successfully"}
    finally:
        connection.close()

@app.put("/bubbleteasfromaiven/{id}")
def update_bubble_tea_in_aiven(id: int, bubble_tea: BubbleTeaCreate) -> BubbleTea:
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE bubble_teas SET name = %s, temperature = %s, price = %s, active = %s WHERE id = %s",
                (bubble_tea.name, bubble_tea.temperature, bubble_tea.price, bubble_tea.active, id),
            )
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Bubble tea not found")
            connection.commit()
            return BubbleTea(id=id, **bubble_tea.model_dump())
    finally:
        connection.close()

def filter_out_inactive_productos() -> list[BubbleTea]:
    return [bubble_tea for bubble_tea in productos if bubble_tea.active]