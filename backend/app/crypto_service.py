import json
import httpx
import asyncio
from typing import List, Optional
from datetime import datetime
from app.cache import cache

COINGECKO_API_URL = "https://api.coingecko.com/api/v3"

# Auto map common symbols to CoinGecko IDs
CRYPTO_IDS = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "BNB": "binancecoin",
    "XRP": "ripple",
    "ADA": "cardano",
    "SOL": "solana",
    "DOT": "polkadot",
    "MATIC": "matic-network",
    # Add more symbols here
}

class CryptoService:

    @staticmethod
    async def fetch_prices(symbols: List[str]) -> dict:
        """Fetch prices from CoinGecko API and return dict"""
        ids = [CRYPTO_IDS.get(s.upper()) for s in symbols if s.upper() in CRYPTO_IDS]
        ids = [i for i in ids if i]

        if not ids:
            return {s: None for s in symbols}

        url = f"{COINGECKO_API_URL}/simple/price"
        params = {
            "ids": ",".join(ids),
            "vs_currencies": "usd",
            "include_market_cap": "true",
            "include_24hr_vol": "true",
            "include_24hr_change": "true"
        }

        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(url, params=params)
            data = response.json() if response.status_code == 200 else {}

        results = {}
        for symbol in symbols:
            coin_id = CRYPTO_IDS.get(symbol.upper())
            if coin_id and coin_id in data:
                coin = data[coin_id]
                price_data = {
                    "symbol": symbol.upper(),
                    "price": coin.get("usd", 0),
                    "market_cap": coin.get("usd_market_cap", 0),
                    "volume_24h": coin.get("usd_24h_vol", 0),
                    "change_24h": coin.get("usd_24h_change", 0),
                    "timestamp": datetime.utcnow().isoformat()
                }
                results[symbol.upper()] = price_data
                # Cache in Redis
                if cache.redis:
                    await cache.set(f"crypto_price:{symbol.upper()}", price_data, ttl=300)
            else:
                results[symbol.upper()] = None

        return results

    @staticmethod
    async def get_price(symbol: str) -> Optional[dict]:
        """Get price from cache or fetch fresh"""
        symbol = symbol.upper()
        cached = await cache.get(f"crypto_price:{symbol}") if cache.redis else None
        if cached:
            return cached
        prices = await CryptoService.fetch_prices([symbol])
        return prices.get(symbol)

    @staticmethod
    async def get_prices_bulk(symbols: List[str]) -> dict:
        """Get multiple prices from cache or fetch fresh"""
        results = {}
        for symbol in symbols:
            results[symbol.upper()] = await CryptoService.get_price(symbol)
        return results

    @staticmethod
    def trigger_price_update(symbols: List[str]):
        """Trigger Celery task to update prices"""
        from app.tasks import fetch_and_cache_prices
        fetch_and_cache_prices.delay([s.upper() for s in symbols])