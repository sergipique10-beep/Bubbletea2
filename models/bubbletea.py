from pydantic import BaseModel


class BubbleTeaCreate(BaseModel):
    name: str
    temperature: str
    price: float
    active: bool


class BubbleTea(BubbleTeaCreate):
    id: int
