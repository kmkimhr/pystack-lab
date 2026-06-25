import json

from app.core.redis import redis_client

CACHE_TTL = 60  # 60초


async def get_cache(key: str) -> list | None:
    value = await redis_client.get(key)
    return json.loads(value) if value else None


async def set_cache(key: str, data: list) -> None:
    await redis_client.set(key, json.dumps(data, ensure_ascii=False), ex=CACHE_TTL)


async def delete_cache(key: str) -> None: 
    await redis_client.delete(key)