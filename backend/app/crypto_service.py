import httpx
from typing import Optional, List
from app.cache import cache
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
        mapped_id = SYMBOL_TO_ID.get(coin_id, coin_id)

        # 1️⃣ Try cache
        price = await cache.get(f"crypto_price:{mapped_id}")
        if price:
            return price

        # 2️⃣ Trigger background fetch
        from app.tasks import fetch_and_cache_prices
        fetch_and_cache_prices.delay([mapped_id])

        # 3️⃣ Return fallback response
        return {
            "symbol": mapped_id,
            "price": 0,
            "error": "warming cache"
        }

    @staticmethod
    async def get_prices_bulk(coin_ids: List[str]) -> dict:
        results = {}
        missing = []

        for coin_id in coin_ids:
            coin_id = coin_id.lower()
            mapped_id = SYMBOL_TO_ID.get(coin_id, coin_id)

            price = await cache.get(f"crypto_price:{mapped_id}")

            if not price:
                missing.append(mapped_id)
                price = {
                    "symbol": mapped_id,
                    "price": 0,
                    "error": "warming cache"
                }

            results[coin_id] = price

        # 🔥 Trigger background fetch for missing coins
        if missing:
            from app.tasks import fetch_and_cache_prices
            fetch_and_cache_prices.delay(missing)

        return results