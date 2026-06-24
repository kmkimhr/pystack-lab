from fastapi import APIRouter, Depends

from app.schemas.item import ItemCreate, ItemResponse

router = APIRouter()

fake_db: list[ItemResponse] = []


def get_fake_db():
    return fake_db


@router.post("/items", response_model=ItemResponse)
def create_item(item: ItemCreate, db: list = Depends(get_fake_db)):
    new_item = ItemResponse(id=len(db) + 1, **item.model_dump())
    db.append(new_item)
    return new_item


@router.get("/items", response_model=list[ItemResponse])
def get_items(db: list = Depends(get_fake_db)):
    return db