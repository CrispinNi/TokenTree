import json
import httpx
import asyncio
from datetime import datetime
from app.celery_app import app as celery_app
from app.cache import cache
from app.crypto_service import CryptoService

COINGECKO_API_URL = "https://api.coingecko.com/api/v3"


@celery_app.task(bind=True, max_retries=3)
def fetch_and_cache_prices(self, symbols: list):

    try:

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        async def run():

            await cache.init()

            ids = []
            symbol_map = {}

            for symbol in symbols:

                coin_id = await CryptoService.get_coin_id(symbol)

                if coin_id:
                    ids.append(coin_id)
                    symbol_map[coin_id] = symbol

            if not ids:
                print("No valid symbols")
                return

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

            data = response.json()

            for coin_id, coin_data in data.items():

                symbol = symbol_map.get(coin_id)

                price_data = {
                    "symbol": symbol,
                    "price": coin_data.get("usd"),
                    "market_cap": coin_data.get("usd_market_cap"),
                    "volume_24h": coin_data.get("usd_24h_vol"),
                    "change_24h": coin_data.get("usd_24h_change"),
                    "timestamp": datetime.utcnow().isoformat()
                }

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