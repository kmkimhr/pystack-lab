from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.refresh_token import RefreshToken


async def save_refresh_token(
    db: AsyncSession, token: str, user_id: int, expires_at: datetime
) -> RefreshToken:
    rt = RefreshToken(token=token, user_id=user_id, expires_at=expires_at)
    db.add(rt)
    await db.commit()
    await db.refresh(rt)
    return rt


async def get_refresh_token(db: AsyncSession, token: str) -> RefreshToken | None:
    result = await db.execute(select(RefreshToken).where(RefreshToken.token == token))
    return result.scalars().first()


async def revoke_refresh_token(db: AsyncSession, token: str) -> None:
    rt = await get_refresh_token(db, token)
    if rt:
        rt.is_revoked = True
        await db.commit()
