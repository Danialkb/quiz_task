from redis.asyncio import Redis

from resources.config import settings


async def get_redis() -> Redis:
    redis = Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.CACHE_REDIS_TABLE,
    )
    try:
        yield redis
    finally:
        await redis.close()
