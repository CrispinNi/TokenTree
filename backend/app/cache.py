import os
import json
from typing import Any, Optional

from redis.asyncio import Redis
import redis.exceptions

class RedisCache:
    def __init__(self):
        self.redis: Optional[Redis] = None

    async def init(self):
        """Initialize Redis safely"""
        redis_url = os.getenv("REDIS_URL")

        if not redis_url:
            print("⚠️ REDIS_URL not set, running without cache")
            self.redis = None
            return

        try:
            self.redis = Redis.from_url(redis_url, decode_responses=True)
            await self.redis.ping()
            print("✅ Redis connected")
        except Exception as e:
            print("❌ Redis connection failed:", e)
            self.redis = None

    async def close(self):
        if self.redis:
            try:
                await self.redis.close()
            except Exception:
                pass

    async def get(self, key: str) -> Optional[Any]:
        if not self.redis:
            return None
        try:
            value = await self.redis.get(key)
            if value:
                return json.loads(value)
        except redis.exceptions.RedisError:
            return None
        return None

    async def set(self, key: str, value: Any, ttl: int = 600):
        if not self.redis:
            return
        try:
            data = json.dumps(value) if not isinstance(value, str) else value
            await self.redis.setex(key, ttl, data)
        except redis.exceptions.RedisError:
            pass

    async def publish(self, channel: str, message: str):
        if not self.redis:
            return
        try:
            await self.redis.publish(channel, message)
        except redis.exceptions.RedisError:
            pass

# global cache instance
cache = RedisCache()