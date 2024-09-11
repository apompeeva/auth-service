from fastapi import Depends
from redis import Redis  # type: ignore


async def get_redis_pool():
    """Функция для создания пула подключений к Redis."""
    redis = Redis.from_url(
        'redis://redis-1:6379/2',
        encoding='utf8',
        decode_responses=True,
    )
    try:
        yield redis
    finally:
        redis.close()


async def get_redis(redis_pool: Redis = Depends(get_redis_pool)) -> Redis:
    """Зависимость для получения подключения к Redis."""
    return redis_pool
