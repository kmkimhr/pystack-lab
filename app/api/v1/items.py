from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories import item as item_repo
from app.schemas.item import ItemCreate, ItemResponse

router = APIRouter()


@router.post("/items", response_model=ItemResponse)
async def create_item(item: ItemCreate, db: AsyncSession = Depends(get_db)):
    return await item_repo.create_item(db, **item.model_dump())


@router.get("/items", response_model=list[ItemResponse])
async def get_items(db: AsyncSession = Depends(get_db)):
    return await item_repo.get_items(db)


@router.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int, db: AsyncSession = Depends(get_db)):
    item = await item_repo.get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="아이템을 찾을 수 없습니다")
    return item