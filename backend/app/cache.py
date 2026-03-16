import json
import os
from typing import Any, Optional

from redis.asyncio import Redis
import redis.exceptions


class RedisCache:
    def __init__(self):
        self.redis: Optional[Redis] = None


    async def init(self):
        redis_url = os.getenv("REDIS_URL")

        if not redis_url:
            raise RuntimeError("REDIS_URL environment variable not set")

        try:
            self.redis = Redis.from_url(
            redis_url,
            decode_responses=True
        )

            await self.redis.ping()

            print("✅ Redis connected")

        except Exception as e:
            print("❌ Redis connection failed:", e)
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
        """Set value in cache with TTL"""
        if not self.redis:
            return

        try:
            data = json.dumps(value) if not isinstance(value, str) else value
            await self.redis.setex(key, ttl, data)

        except redis.exceptions.RedisError:
            pass

    async def delete(self, key: str):
        if not self.redis:
            return

        try:
            await self.redis.delete(key)
        except redis.exceptions.RedisError:
            pass

    async def exists(self, key: str) -> bool:
        if not self.redis:
            return False

        try:
            return (await self.redis.exists(key)) > 0
        except redis.exceptions.RedisError:
            return False

    async def publish(self, channel: str, message: str):
        if not self.redis:
            return

        try:
            await self.redis.publish(channel, message)
        except redis.exceptions.RedisError:
            pass


# global cache instance
cache = RedisCache()