from fastapi import APIRouter, HTTPException
import models.pedido
from utils.db_connection import get_connection


router = APIRouter()


@router.get("/pedidos")
def get_pedidos() -> list[models.pedido.Pedido]:
    with get_connection().cursor() as cursor:
        cursor.execute("SELECT * FROM pedidos")
        result = cursor.fetchall()
        return [models.pedido.Pedido(**row) for row in result]


@router.get("/pedidos/{id}")
def get_pedido(id: int) -> models.pedido.Pedido:
    with get_connection().cursor() as cursor:
        cursor.execute("SELECT * FROM pedidos WHERE id = %s", (id,))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Pedido not found")
        return models.pedido.Pedido(**result)


@router.post("/pedidos")
def create_pedido(pedido: models.pedido.PedidoCreate) -> models.pedido.Pedido:
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO pedidos (bubble_tea_id, cantidad, estado) VALUES (%s, %s, %s)",
            (pedido.bubble_tea_id, pedido.cantidad, pedido.estado),
        )
        conn.commit()
        new_id = cursor.lastrowid
        cursor.execute("SELECT * FROM pedidos WHERE id = %s", (new_id,))
        return models.pedido.Pedido(**cursor.fetchone())


@router.put("/pedidos/{id}")
def update_pedido(id: int, pedido: models.pedido.PedidoCreate) -> models.pedido.Pedido:
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT id FROM pedidos WHERE id = %s", (id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Pedido not found")
        cursor.execute(
            "UPDATE pedidos SET bubble_tea_id = %s, cantidad = %s, estado = %s WHERE id = %s",
            (pedido.bubble_tea_id, pedido.cantidad, pedido.estado, id),
        )
        conn.commit()
        cursor.execute("SELECT * FROM pedidos WHERE id = %s", (id,))
        return models.pedido.Pedido(**cursor.fetchone())


@router.delete("/pedidos/{id}", status_code=204)
def delete_pedido(id: int):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT id FROM pedidos WHERE id = %s", (id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Pedido not found")
        cursor.execute("DELETE FROM pedidos WHERE id = %s", (id,))
        conn.commit()
