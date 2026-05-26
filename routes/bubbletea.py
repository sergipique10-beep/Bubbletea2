from fastapi import APIRouter, HTTPException
import models.bubbletea
from utils.db_connection import get_connection


router = APIRouter()


@router.get("/bubbleteas")
def get_productos() -> list[models.bubbletea.BubbleTea]:
    with get_connection().cursor() as cursor:
        cursor.execute("SELECT * FROM bubble_teas WHERE active = 1")
        result = cursor.fetchall()
        return [models.bubbletea.BubbleTea(**row) for row in result]


@router.get("/bubbleteasfromaiven/{id}")
def get_bubble_tea_from_aiven(id: int) -> models.bubbletea.BubbleTea:
    with get_connection().cursor() as cursor:
        cursor.execute("SELECT * FROM bubble_teas WHERE id = %s AND active = 1", (id,))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Bubble tea not found")
        return models.bubbletea.BubbleTea(**result)


@router.get("/bubbleteasfromaiven")
def get_productos_from_aiven() -> list[models.bubbletea.BubbleTea]:
    with get_connection().cursor() as cursor:
        cursor.execute("SELECT * FROM bubble_teas WHERE active = 1")
        result = cursor.fetchall()
        return [models.bubbletea.BubbleTea(**row) for row in result]


@router.post("/bubbleteasfromaiven")
def add_bubble_tea_to_aiven(bubble_tea: models.bubbletea.BubbleTeaCreate) -> models.bubbletea.BubbleTea:
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO bubble_teas (name, temperature, price, active) VALUES (%s, %s, %s, %s)",
            (bubble_tea.name, bubble_tea.temperature, bubble_tea.price, bubble_tea.active),
        )
        conn.commit()
        return models.bubbletea.BubbleTea(id=cursor.lastrowid, **bubble_tea.model_dump())


@router.delete("/bubbleteasfromaiven/{id}")
def soft_delete_bubble_tea_from_aiven(id: int):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("UPDATE bubble_teas SET active = 0 WHERE id = %s", (id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Bubble tea not found")
        conn.commit()
        return {"message": "Bubble tea soft-deleted successfully"}


@router.put("/bubbleteasfromaiven/{id}")
def update_bubble_tea_in_aiven(id: int, bubble_tea: models.bubbletea.BubbleTeaCreate) -> models.bubbletea.BubbleTea:
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute(
            "UPDATE bubble_teas SET name = %s, temperature = %s, price = %s, active = %s WHERE id = %s",
            (bubble_tea.name, bubble_tea.temperature, bubble_tea.price, bubble_tea.active, id),
        )
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Bubble tea not found")
        conn.commit()
        return models.bubbletea.BubbleTea(id=id, **bubble_tea.model_dump())
