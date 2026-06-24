from fastapi import APIRouter, Depends, HTTPException
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


@router.get("/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, db: list = Depends(get_fake_db)):
    for item in db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="아이템을 찾을 수 없습니다")
