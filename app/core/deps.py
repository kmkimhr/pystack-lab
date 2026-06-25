from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.user import User
from app.repositories import user as user_repo

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    email = decode_access_token(token)
    if not email:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다")
    user = await user_repo.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다")
    return user
