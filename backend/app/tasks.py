import json
import httpx
from app.celery_app import app as celery_app
from app.cache import cache
from datetime import datetime
import asyncio

COINGECKO_API_URL = "https://api.coingecko.com/api/v3"

CRYPTO_IDS = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "BNB": "binancecoin",
    "XRP": "ripple",
    "ADA": "cardano",
    "SOL": "solana",
    "DOT": "polkadot",
    "MATIC": "matic-network",
}


async def fetch_all_prices(symbols: list) -> dict:
    """Fetch prices from CoinGecko"""

    ids = [CRYPTO_IDS[s] for s in symbols if s in CRYPTO_IDS]

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{COINGECKO_API_URL}/simple/price",
            params={
                "ids": ",".join(ids),
                "vs_currencies": "usd",
                "include_market_cap": "true",
                "include_24hr_vol": "true",
                "include_24hr_change": "true"
            },
            timeout=10
        )

        response.raise_for_status()
        data = response.json()

    results = {}

    for symbol in symbols:
        coin_id = CRYPTO_IDS.get(symbol)

        if coin_id and coin_id in data:

            coin = data[coin_id]

            results[symbol] = {
                "symbol": symbol,
                "price": coin.get("usd", 0),
                "market_cap": coin.get("usd_market_cap", 0),
                "volume_24h": coin.get("usd_24h_vol", 0),
                "change_24h": coin.get("usd_24h_change", 0),
                "timestamp": datetime.utcnow().isoformat()
            }

    return results


@celery_app.task(bind=True, max_retries=3)
def fetch_and_cache_prices(self, symbols: list):

    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        async def run():

            await cache.init()

            prices = await fetch_all_prices(symbols)

            for symbol, price_data in prices.items():

                await cache.set(
                    f"crypto_price:{symbol}",
                    price_data,
                    ttl=300
                )

                await cache.publish(
                    f"price_updates:{symbol}",
                    json.dumps(price_data)
                )

                print(f"Updated {symbol}: ${price_data['price']}")

            await cache.close()

        loop.run_until_complete(run())

    except Exception as e:

        print("Price update failed:", e)

        raise self.retry(countdown=60)

    return {"status": "completed"}