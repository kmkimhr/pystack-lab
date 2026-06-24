from pydantic import BaseModel


class ItemCreate(BaseModel):
    name: str
    price: float
    is_available: bool = True


class ItemResponse(BaseModel):
    id: int
    name: str
    price: float
    is_available: bool