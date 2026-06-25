import secrets
from datetime import datetime, timedelta, timezone

import bcrypt
from jose import jwt

from app.core.config import settings


# 회원가입 시 평문 비밀번호를 bcrypt 해시로 변환 → DB에 저장
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


# 로그인 시 입력된 평문과 DB의 해시값 비교 → True/False 반환
def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())


# 로그인 성공 후 subject(email 등)를 담은 JWT 액세스 토큰 발급
def create_access_token(subject: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expire_minutes)
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(
        payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm
    )


# 요청마다 토큰 검증 후 subject 반환, 만료/서명오류 시 None 반환
def decode_access_token(token: str) -> str | None:
    try:
        payload = jwt.decode(
            token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm]
        )
        return payload.get("sub")
    except Exception:
        return None


def create_refresh_token() -> tuple[str, datetime]:
    token = secrets.token_urlsafe(32)
    expires_at = datetime.now(timezone.utc) + timedelta(
        days=settings.jwt_refresh_expire_days
    )
    return token, expires_at
