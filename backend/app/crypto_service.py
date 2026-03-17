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

    # FIX: Fetch immediately instead of just returning None
        print(f"Cache miss for {coin_id}, fetching now...")
        price = await CryptoService.fetch_price_now(coin_id)
    
    # Still trigger background task for future updates if desired
        from app.tasks import fetch_and_cache_prices
        fetch_and_cache_prices.delay([coin_id])

        return price

    @staticmethod
    async def fetch_price_now(coin_id: str):
        url = f"{COINGECKO_API_URL}/simple/price"

        params = {
        "ids": coin_id,
        "vs_currencies": "usd",
        "include_market_cap": "true",
        "include_24hr_vol": "true",
        "include_24hr_change": "true"
        }

        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(url, params=params)

        data = response.json()

        if coin_id not in data:
            return None

        coin_data = data[coin_id]

        price_data = {
        "symbol": coin_id,
        "price": coin_data.get("usd"),
        "market_cap": coin_data.get("usd_market_cap"),
        "volume_24h": coin_data.get("usd_24h_vol"),
        "change_24h": coin_data.get("usd_24h_change"),
        }

        await cache.set(f"crypto_price:{coin_id}", price_data, ttl=300)

        return price_data
    

    @staticmethod
    async def get_prices_bulk(coin_ids: List[str]) -> dict:
        results = {}

        for coin_id in coin_ids:
            coin_id = coin_id.lower()

        # FIX: Move these lines INSIDE the for loop indentation
            price = await cache.get(f"crypto_price:{coin_id}")

            if not price:
            # fetch immediately if cache empty
                price = await CryptoService.fetch_price_now(coin_id)

            # also trigger background refresh
                from app.tasks import fetch_and_cache_prices
                fetch_and_cache_prices.delay([coin_id])

            results[coin_id] = price

        return results


    @staticmethod
    def trigger_price_update(coin_ids: List[str]):

        from app.tasks import fetch_and_cache_prices
        fetch_and_cache_prices.delay(coin_ids)