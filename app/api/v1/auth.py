from datetime import timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)
from app.repositories import refresh_token as rt_repo
from app.repositories import user as user_repo
from app.schemas.user import RefreshRequest, Token, UserCreate, UserResponse

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    existing = await user_repo.get_user_by_email(db, user.email)
    if existing:
        raise HTTPException(status_code=400, detail="이미 사용 중인 이메일입니다")
    return await user_repo.create_user(db, user.email, hash_password(user.password))


@router.post("/login", response_model=Token)
async def login(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await user_repo.get_user_by_email(db, user.email)
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=401, detail="이메일 또는 비밀번호가 올바르지 않습니다"
        )
    refresh_token, expires_at = create_refresh_token()
    await rt_repo.save_refresh_token(db, refresh_token, db_user.id, expires_at)
    return Token(
        access_token=create_access_token(db_user.email),
        refresh_token=refresh_token,
    )


@router.post("/refresh", response_model=Token)
async def refresh(body: RefreshRequest, db: AsyncSession = Depends(get_db)):
    from datetime import datetime

    rt = await rt_repo.get_refresh_token(db, body.refresh_token)
    if not rt or rt.is_revoked:
        raise HTTPException(status_code=401, detail="유효하지 않은 리프레시 토큰입니다")
    if rt.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail="만료된 리프레시 토큰입니다")

    user = await user_repo.get_user_by_id(db, rt.user_id)

    await rt_repo.revoke_refresh_token(db, body.refresh_token)
    new_refresh_token, expires_at = create_refresh_token()
    await rt_repo.save_refresh_token(db, new_refresh_token, rt.user_id, expires_at)
    return Token(
        access_token=create_access_token(user.email),
        refresh_token=new_refresh_token,
    )


@router.post("/logout", status_code=204)
async def logout(body: RefreshRequest, db: AsyncSession = Depends(get_db)):
    await rt_repo.revoke_refresh_token(db, body.refresh_token)

