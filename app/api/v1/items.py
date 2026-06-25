from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories import item as item_repo
from app.schemas.item import ItemCreate, ItemResponse, ItemUpdate

router = APIRouter()


@router.post("/items", response_model=ItemResponse, status_code=201)
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


@router.put("/items/{item_id}", response_model=ItemResponse)
async def update_item(
    item_id: int, item: ItemUpdate, db: AsyncSession = Depends(get_db)
):
    updated = await item_repo.update_item(
        db, item_id, item.model_dump(exclude_none=True)
    )
    if not updated:
        raise HTTPException(status_code=404, detail="아이템을 찾을 수 없습니다")
    return updated


@router.delete("/items/{item_id}", status_code=204)
async def delete_item(item_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await item_repo.delete_item(db, item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="아이템을 찾을 수 없습니다")
