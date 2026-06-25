from app.core.redis import redis_client

REFRESH_TOKEN_PREFIX = "rt:"


async def save_refresh_token(token: str, user_id: int, expire_seconds: int) -> None:
    await redis_client.set(f"{REFRESH_TOKEN_PREFIX}{token}", user_id, ex=expire_seconds)


async def get_user_id_by_refresh_token(token: str) -> int | None:
    value = await redis_client.get(f"{REFRESH_TOKEN_PREFIX}{token}")
    return int(value) if value else None


async def revoke_refresh_token(token: str) -> None:
    await redis_client.delete(f"{REFRESH_TOKEN_PREFIX}{token}")
