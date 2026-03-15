from app.cache import cache
from typing import Optional, List


class CryptoService:

    @staticmethod
    async def get_price(symbol: str) -> Optional[dict]:
        """Get crypto price from Redis cache"""

        price = await cache.get(f"crypto_price:{symbol}")
        return price


    @staticmethod
    async def get_prices_bulk(symbols: List[str]) -> dict:
        """Get multiple prices from cache"""

        results = {}

        for symbol in symbols:
            results[symbol] = await cache.get(f"crypto_price:{symbol}")

        return results


    @staticmethod
    def trigger_price_update(symbols: List[str]):
        """Trigger Celery background update"""

        from app.tasks import fetch_and_cache_prices
        fetch_and_cache_prices.delay(symbols)