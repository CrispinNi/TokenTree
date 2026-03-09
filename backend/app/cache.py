import json
from typing import Any, Optional
from redis.asyncio import Redis
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")


class RedisCache:
    def __init__(self):
        self.redis = None

    async def init(self):
        """Initialize Redis connection"""
        self.redis = await Redis.from_url(REDIS_URL, decode_responses=True)

    async def close(self):
        """Close Redis connection"""
        if self.redis:
            await self.redis.close()

    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if not self.redis:
            return None
        value = await self.redis.get(key)
        if value:
            try:
                return json.loads(value)
            except:
                return value
        return None

    async def set(self, key: str, value: Any, ttl: int = 300):
        """Set value in cache with TTL (default 5 minutes)"""
        if not self.redis:
            return
        await self.redis.setex(
            key,
            ttl,
            json.dumps(value) if not isinstance(value, str) else value
        )

    async def delete(self, key: str):
        """Delete value from cache"""
        if not self.redis:
            return
        await self.redis.delete(key)

    async def exists(self, key: str) -> bool:
        """Check if key exists"""
        if not self.redis:
            return False
        return await self.redis.exists(key) > 0

    async def publish(self, channel: str, message: str):
        """Publish message to Redis pub/sub"""
        if not self.redis:
            return
        await self.redis.publish(channel, message)


# Global cache instance
cache = RedisCache()