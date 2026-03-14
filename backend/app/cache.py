import json
import os
from typing import Any, Optional
from redis.asyncio import Redis
import redis.exceptions

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")


class RedisCache:
    def __init__(self):
        self.redis: Optional[Redis] = None

    async def init(self):
        """Initialize Redis connection safely"""
        try:
            self.redis = Redis.from_url(REDIS_URL, decode_responses=True)

            # test connection
            await self.redis.ping()

            print("✅ Redis connected:", REDIS_URL)

        except Exception as e:
            print("⚠️ Redis unavailable, running without cache:", e)
            self.redis = None

    async def close(self):
        """Close Redis connection"""
        if self.redis:
            try:
                await self.redis.close()
            except Exception:
                pass

    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if not self.redis:
            return None

        try:
            value = await self.redis.get(key)

            if value:
                try:
                    return json.loads(value)
                except Exception:
                    return value

        except redis.exceptions.RedisError:
            return None

        return None

    async def set(self, key: str, value: Any, ttl: int = 600):
        """Set value in cache with TTL (default 10 minutes)"""
        if not self.redis:
            return

        try:
            await self.redis.setex(
                key,
                ttl,
                json.dumps(value) if not isinstance(value, str) else value,
            )
        except redis.exceptions.RedisError:
            pass

    async def delete(self, key: str):
        """Delete value from cache"""
        if not self.redis:
            return

        try:
            await self.redis.delete(key)
        except redis.exceptions.RedisError:
            pass

    async def exists(self, key: str) -> bool:
        """Check if key exists"""
        if not self.redis:
            return False

        try:
            return await self.redis.exists(key) > 0
        except redis.exceptions.RedisError:
            return False

    async def publish(self, channel: str, message: str):
        """Publish message to Redis pub/sub"""
        if not self.redis:
            return

        try:
            await self.redis.publish(channel, message)
        except redis.exceptions.RedisError:
            pass


# Global cache instance
cache = RedisCache()