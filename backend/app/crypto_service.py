import httpx
import asyncio
from datetime import datetime
from typing import Optional, List
from app.cache import cache

COINGECKO_API_URL = "https://api.coingecko.com/api/v3"
COINCAP_API_URL = "https://api.coincap.io/v2"

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
    async def get_price(symbol: str) -> dict:
        symbol = symbol.lower()
        coin_id = SYMBOL_TO_ID.get(symbol, symbol)

    # 1️⃣ Check cache
        price = await cache.get(f"crypto_price:{coin_id}")
        if price:
            return price

        print(f"Cache miss for {coin_id}, fetching now...")

    # 2️⃣ Fetch immediately (FIXED HERE)
        price = await CryptoService.fetch_price(coin_id)

    # 3️⃣ Background refresh (non-blocking)
        asyncio.create_task(CryptoService.refresh_price(coin_id))

    # 4️⃣ Fallback
        if not price:
            return {
            "symbol": coin_id,
            "price": 0,
            "error": "Price not available yet (warming cache)"
           }

        return price

    @staticmethod
    async def fetch_price(coin_id: str) -> Optional[dict]:
        """Try CoinGecko first, then CoinCap fallback."""
        providers = [
            CryptoService._fetch_coingecko,
            CryptoService._fetch_coincap
        ]
        for provider in providers:
            try:
                data = await provider(coin_id)
                if data:
                    # Save to Redis
                    await cache.set(f"crypto_price:{coin_id}", data, ttl=300)
                    return data
            except Exception as e:
                print(f"{provider.__name__} failed: {e}")
        return None

    @staticmethod
    async def refresh_price(coin_id: str):
        """Background refresh without blocking response."""
        await CryptoService.fetch_price(coin_id)

    @staticmethod
    async def _fetch_coingecko(coin_id: str) -> Optional[dict]:
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
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get(url, params=params)
            if resp.status_code == 429:
                await asyncio.sleep(2 ** attempt)
                continue
            if resp.status_code != 200:
                return None
            data = resp.json()
            if coin_id not in data:
                return None
            coin = data[coin_id]
            return {
                "symbol": coin_id,
                "price": coin.get("usd"),
                "market_cap": coin.get("usd_market_cap"),
                "volume_24h": coin.get("usd_24h_vol"),
                "change_24h": coin.get("usd_24h_change"),
                "timestamp": datetime.utcnow().isoformat()
            }
        return None

    @staticmethod
    async def _fetch_coincap(coin_id: str) -> Optional[dict]:
        # Map CoinGecko ID → CoinCap ID (rough mapping)
        COINCAP_MAPPING = {
            "bitcoin": "bitcoin",
            "ethereum": "ethereum",
            "binancecoin": "binance-coin",
            "ripple": "ripple",
            "cardano": "cardano",
            "solana": "solana",
            "polkadot": "polkadot",
            "polygon": "matic-network"
        }
        coin = COINCAP_MAPPING.get(coin_id, coin_id)
        url = f"{COINCAP_API_URL}/assets/{coin}"
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(url)
        if resp.status_code != 200:
            return None
        data = resp.json().get("data", {})
        if not data:
            return None
        return {
            "symbol": coin_id,
            "price": float(data.get("priceUsd", 0)),
            "market_cap": float(data.get("marketCapUsd", 0)),
            "volume_24h": float(data.get("volumeUsd24Hr", 0)),
            "change_24h": float(data.get("changePercent24Hr", 0)),
            "timestamp": datetime.utcnow().isoformat()
        }

    @staticmethod
    async def get_prices_bulk(symbols: List[str]) -> dict:
        results = {}
        for s in symbols:
            s = s.lower()
            results[s] = await CryptoService.get_price(s)
        return results