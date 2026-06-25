from pydantic import BaseModel
from pydantic import ConfigDict


class ItemCreate(BaseModel):
    name: str
    price: float
    is_available: bool = True


class ItemUpdate(BaseModel):
    name: str | None = None
    price: float | None = None
    is_available: bool | None = None


class ItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    price: float
    is_available: bool