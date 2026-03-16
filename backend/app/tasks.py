import json
import httpx
from app.celery_app import app as celery_app
from app.cache import cache
from datetime import datetime
import asyncio

COINGECKO_API_URL = "https://api.coingecko.com/api/v3"

# symbol → coingecko id
CRYPTO_MAP = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "SOL": "solana",
    "BNB": "binancecoin",
    "XRP": "ripple",
    "ADA": "cardano",
}

class CryptoService:

    @staticmethod
    async def get_prices(symbols: List[str]):

        ids = []
        symbol_map = {}

        for symbol in symbols:
            sym = symbol.upper()

            if sym in CRYPTO_MAP:
                coin_id = CRYPTO_MAP[sym]
                ids.append(coin_id)
                symbol_map[coin_id] = sym

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

        if response.status_code != 200:
            print("CoinGecko error:", response.text)
            return {s: None for s in symbols}

        data = response.json()

        results = {}

        for coin_id, coin_data in data.items():

            symbol = symbol_map.get(coin_id)

            results[symbol] = {
                "symbol": symbol,
                "price": coin_data.get("usd"),
                "market_cap": coin_data.get("usd_market_cap"),
                "volume_24h": coin_data.get("usd_24h_vol"),
                "change_24h": coin_data.get("usd_24h_change"),
                "timestamp": datetime.utcnow().isoformat()
            }

            await cache.set(f"crypto_price:{symbol}", results[symbol], ttl=300)

        return results

@celery_app.task(bind=True, max_retries=3)
def fetch_and_cache_prices(self, symbols: list):

    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        async def run():

            await cache.init()

            prices = await CryptoService.get_prices(symbols)

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