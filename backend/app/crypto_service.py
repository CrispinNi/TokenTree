import httpx
from typing import Optional, List
from app.cache import cache
import asyncio
from datetime import datetime

COINGECKO_API_URL = "https://api.coingecko.com/api/v3"

SYMBOL_TO_ID = {
    "btc": "bitcoin",
    "eth": "ethereum",
    "bnb": "binancecoin",
    "xrp": "ripple",
    "ada": "cardano",
    "sol": "solana",
    "dot": "polkadot",
    "matic": "polygon"
}


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
        coin_id = coin_id.lower()

    # Map symbol → CoinGecko ID
        coin_id = SYMBOL_TO_ID.get(coin_id, coin_id)

        url = f"{COINGECKO_API_URL}/simple/price"

        params = {
           "ids": coin_id,
           "vs_currencies": "usd",
           "include_market_cap": "true",
           "include_24hr_vol": "true",
           "include_24hr_change": "true"
    }

        retries = 3

        for attempt in range(retries):
            try:
                async with httpx.AsyncClient(timeout=10) as client:
                    response = await client.get(url, params=params)

                print(f"Attempt {attempt+1}: STATUS {response.status_code}")

            # 🚨 HANDLE RATE LIMIT
                if response.status_code == 429:
                    wait_time = 2 ** attempt
                    print(f"Rate limited. Retrying in {wait_time}s...")
                    await asyncio.sleep(wait_time)
                    continue

                if response.status_code != 200:
                    return None

                data = response.json()

                if not data or coin_id not in data:
                    return None

                coin_data = data[coin_id]

                price_data = {
                "symbol": coin_id,
                "price": coin_data.get("usd"),
                "market_cap": coin_data.get("usd_market_cap"),
                "volume_24h": coin_data.get("usd_24h_vol"),
                "change_24h": coin_data.get("usd_24h_change"),
                "timestamp": datetime.utcnow().isoformat()
            }

            # Save to Redis
                await cache.set(f"crypto_price:{coin_id}", price_data, ttl=300)

                return price_data

            except Exception as e:
                print("Fetch error:", e)
                await asyncio.sleep(1)

        return None
    

    @staticmethod
    async def get_prices_bulk(coin_ids: List[str]) -> dict:
        results = {}

        for coin_id in coin_ids:
            coin_id = coin_id.lower()
            mapped_id = SYMBOL_TO_ID.get(coin_id, coin_id)

        # ONLY read from cache
            price = await cache.get(f"crypto_price:{mapped_id}")

            if not price:
                price = {
                "symbol": mapped_id,
                "price": 0,
                "error": "Price not available yet (warming cache)"
            }

            results[coin_id] = price

        return results


    @staticmethod
    def trigger_price_update(coin_ids: List[str]):

        from app.tasks import fetch_and_cache_prices
        fetch_and_cache_prices.delay(coin_ids)