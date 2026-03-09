import json
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential
from app.celery_app import app as celery_app
from app.cache import cache
from datetime import datetime
import asyncio
import os

COINGECKO_API_URL = "https://api.coingecko.com/api/v3"

# Mapping of symbols to CoinGecko IDs
CRYPTO_IDS = {
    'BTC': 'bitcoin',
    'ETH': 'ethereum',
    'BNB': 'binancecoin',
    'XRP': 'ripple',
    'ADA': 'cardano',
    'SOL': 'solana',
    'DOT': 'polkadot',
    'MATIC': 'matic-network',
}


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
async def fetch_crypto_price(symbol: str) -> dict:
    """Fetch crypto price from CoinGecko API with retries"""
    if symbol not in CRYPTO_IDS:
        return None

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{COINGECKO_API_URL}/simple/price",
                params={
                    "ids": CRYPTO_IDS[symbol],
                    "vs_currencies": "usd",
                    "include_market_cap": "true",
                    "include_24hr_vol": "true",
                    "include_24hr_change": "true"
                },
                timeout=10.0
            )
            response.raise_for_status()
            data = response.json()
            
            # Transform response
            crypto_id = CRYPTO_IDS[symbol]
            if crypto_id in data:
                return {
                    "symbol": symbol,
                    "price": data[crypto_id].get("usd", 0),
                    "market_cap": data[crypto_id].get("usd_market_cap", 0),
                    "volume_24h": data[crypto_id].get("usd_24h_vol", 0),
                    "change_24h": data[crypto_id].get("usd_24h_change", 0),
                    "timestamp": datetime.utcnow().isoformat()
                }
        except Exception as e:
            print(f"Error fetching {symbol}: {e}")
            raise


@celery_app.task(bind=True, max_retries=3)
def fetch_and_cache_prices(self, symbols: list):
    """Background task to fetch and cache crypto prices"""
    try:
        # Run async function in event loop
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    async def _fetch_all():
        await cache.init()
        
        for symbol in symbols:
            try:
                price_data = await fetch_crypto_price(symbol)
                if price_data:
                    # Cache for 5 minutes (300 seconds)
                    await cache.set(
                        f"crypto_price:{symbol}",
                        price_data,
                        ttl=300
                    )
                    
                    # Publish to WebSocket subscribers
                    await cache.publish(
                        f"price_updates:{symbol}",
                        json.dumps(price_data)
                    )
                    print(f"Updated {symbol}: ${price_data['price']}")
            except Exception as e:
                print(f"Failed to fetch {symbol}: {e}")
                # Retry the task
                raise self.retry(exc=e, countdown=60)
        
        await cache.close()

    loop.run_until_complete(_fetch_all())
    return {"status": "completed", "symbols": symbols}
