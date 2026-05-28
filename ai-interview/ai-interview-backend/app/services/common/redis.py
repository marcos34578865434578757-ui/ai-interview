from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

try:
    from redis.asyncio import Redis
except ImportError:
    Redis = None


class RedisClient:
    def __init__(self):
        self.redis = None
        host = getattr(settings, "REDIS_HOST", "")
        if not host or host.strip() == "":
            logger.warning("Redis not configured, running without Redis")
            return
        try:
            redis_params = {
                "host": host,
                "port": getattr(settings, "REDIS_PORT", 6379),
                "decode_responses": True,
                "socket_connect_timeout": 2,
            }
            password = getattr(settings, "REDIS_PASSWORD", "")
            if password:
                redis_params["password"] = password
            self.redis = Redis(**redis_params)
        except Exception as e:
            logger.warning(f"Redis init failed: {e}")
            self.redis = None

    async def set_with_ttl(self, key: str, value: str, ttl_seconds: int):
        if not self.redis: return
        try:
            await self.redis.setex(key, ttl_seconds, value)
        except Exception:
            pass

    async def get(self, key: str) -> str:
        if not self.redis: return None
        try:
            return await self.redis.get(key)
        except Exception:
            return None

    async def delete(self, key: str):
        if not self.redis: return
        try:
            await self.redis.delete(key)
        except Exception:
            pass

    async def set_cooldown(self, key: str, ttl_seconds: int):
        if not self.redis: return
        try:
            await self.redis.setex(key, ttl_seconds, "1")
        except Exception:
            pass

    async def check_cooldown(self, key: str) -> bool:
        if not self.redis: return False
        try:
            return bool(await self.redis.exists(key))
        except Exception:
            return False

    def pipeline(self, *args, **kwargs):
        if not self.redis: return None
        try:
            return self.redis.pipeline(*args, **kwargs)
        except Exception:
            return None

    async def brpop(self, key, timeout=1):
        if not self.redis: return None
        try:
            return await self.redis.brpop(key, timeout=timeout)
        except Exception:
            return None

    async def close(self):
        if not self.redis: return
        try:
            await self.redis.close()
        except Exception:
            pass


redis_client = RedisClient()
