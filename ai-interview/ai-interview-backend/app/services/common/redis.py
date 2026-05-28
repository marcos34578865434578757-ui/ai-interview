from redis.asyncio import Redis
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class RedisClient:
    def __init__(self):
        self.redis = None
        if not settings.REDIS_HOST:
            logger.warning("Redis not configured, running without Redis")
            return
        try:
            redis_params = {
                "host": settings.REDIS_HOST,
                "port": settings.REDIS_PORT,
                "decode_responses": True
            }
            if hasattr(settings, "REDIS_PASSWORD") and settings.REDIS_PASSWORD:
                redis_params["password"] = settings.REDIS_PASSWORD
            self.redis = Redis(**redis_params)
        except Exception as e:
            logger.warning(f"Redis init failed: {e}")

    async def set_with_ttl(self, key: str, value: str, ttl_seconds: int):
        if not self.redis: return
        await self.redis.setex(key, ttl_seconds, value)

    async def get(self, key: str) -> str:
        if not self.redis: return None
        return await self.redis.get(key)

    async def delete(self, key: str):
        if not self.redis: return
        await self.redis.delete(key)

    async def set_cooldown(self, key: str, ttl_seconds: int):
        if not self.redis: return
        await self.redis.setex(key, ttl_seconds, "1")

    async def check_cooldown(self, key: str) -> bool:
        if not self.redis: return False
        return bool(await self.redis.exists(key))

    def pipeline(self, *args, **kwargs):
        if not self.redis: return None
        return self.redis.pipeline(*args, **kwargs)

    async def brpop(self, key, timeout=1):
        if not self.redis: return None
        return await self.redis.brpop(key, timeout=timeout)

    async def close(self):
        if not self.redis: return
        try:
            await self.redis.close()
        except Exception:
            pass


redis_client = RedisClient()
