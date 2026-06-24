from fastapi import APIRouter

from app.schemas.item import ItemCreate, ItemResponse

router = APIRouter()

fake_db: list[ItemResponse] = []

@router.post("/items", response_model=ItemResponse)
def create_item(item: ItemCreate):
    new_item = ItemResponse(id=len(fake_db) + 1, **item.model_dump())
    fake_db.append(new_item)
    return new_item


@router.get("/items", response_model=list[ItemResponse])
def get_items():
    return fake_db