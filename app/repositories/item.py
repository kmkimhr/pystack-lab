from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.item import Item


async def get_items(db: AsyncSession) -> list[Item]:
    result = await db.execute(select(Item))
    return list(result.scalars().all())


async def get_item(db: AsyncSession, item_id: int) -> Item | None:
    result = await db.execute(select(Item).where(Item.id == item_id))
    return result.scalars().first()


async def create_item(db: AsyncSession, name: str, price: float, is_available: bool) -> Item:
    item = Item(name=name, price=price, is_available=is_available)
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item