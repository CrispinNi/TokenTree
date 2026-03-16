import httpx
from typing import Optional, List
from app.cache import cache

COINGECKO_API_URL = "https://api.coingecko.com/api/v3"


class CryptoService:

    @staticmethod
    async def get_price(coin_id: str) -> Optional[dict]:

        coin_id = coin_id.lower()

        price = await cache.get(f"crypto_price:{coin_id}")

        if price:
            return price

        from app.tasks import fetch_and_cache_prices
        fetch_and_cache_prices.delay([coin_id])

        return None


    @staticmethod
    async def get_prices_bulk(coin_ids: List[str]) -> dict:

        results = {}

        for coin_id in coin_ids:

            coin_id = coin_id.lower()

            price = await cache.get(f"crypto_price:{coin_id}")

            if not price:
                from app.tasks import fetch_and_cache_prices
                fetch_and_cache_prices.delay([coin_id])

            results[coin_id] = price

        return results


    @staticmethod
    def trigger_price_update(coin_ids: List[str]):

        from app.tasks import fetch_and_cache_prices
        fetch_and_cache_prices.delay(coin_ids)