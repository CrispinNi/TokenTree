from app.cache import cache
from app.tasks import fetch_crypto_price, fetch_and_cache_prices
import json
from typing import Optional, List
import asyncio


class CryptoService:
    @staticmethod
    async def get_price(symbol: str) -> Optional[dict]:
        """Get crypto price from cache or fetch fresh"""
        await cache.init()
        
        # Try cache first
        cached = await cache.get(f"crypto_price:{symbol}")
        if cached:
            await cache.close()
            return cached
        
        # If not in cache, fetch fresh (this will be cached by background job)
        try:
            price_data = await fetch_crypto_price(symbol)
            if price_data:
                await cache.set(f"crypto_price:{symbol}", price_data, ttl=300)
            await cache.close()
            return price_data
        except Exception as e:
            await cache.close()
            print(f"Error fetching price for {symbol}: {e}")
            return None

    @staticmethod
    async def get_prices_bulk(symbols: List[str]) -> dict:
        """Get multiple crypto prices"""
        await cache.init()
        
        results = {}
        for symbol in symbols:
            cached = await cache.get(f"crypto_price:{symbol}")
            results[symbol] = cached
        
        await cache.close()
        return results

    @staticmethod
    def trigger_price_update(symbols: List[str]):
        """Manually trigger background job to update prices"""
        fetch_and_cache_prices.delay(symbols)
