from pydantic import BaseModel
from datetime import datetime


class PedidoCreate(BaseModel):
    bubble_tea_id: int
    cantidad: int
    estado: str = "pendiente"


class Pedido(PedidoCreate):
    id: int
    fecha_creacion: datetime
