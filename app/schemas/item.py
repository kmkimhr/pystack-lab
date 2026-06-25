from pydantic import BaseModel
from pydantic import ConfigDict


class ItemCreate(BaseModel):
    name: str
    price: float
    is_available: bool = True


class ItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    price: float
    is_available: bool