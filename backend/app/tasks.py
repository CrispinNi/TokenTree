import json
import httpx
import asyncio
from datetime import datetime
from app.celery_app import app as celery_app
from app.cache import cache

COINGECKO_API_URL = "https://api.coingecko.com/api/v3"


async def fetch_prices(ids: list):
    results = {}

    # =========================
    # 1️⃣ CoinGecko (Primary)
    # =========================
    try:
        url = f"{COINGECKO_API_URL}/simple/price"
        params = {
            "ids": ",".join(ids),
            "vs_currencies": "usd",
            "include_market_cap": "true",
            "include_24hr_vol": "true",
            "include_24hr_change": "true"
        }

        async with httpx.AsyncClient(timeout=10) as client:
            res = await client.get(url, params=params)

        if res.status_code == 200:
            data = res.json()

            for coin_id, coin_data in data.items():
                results[coin_id] = {
                    "symbol": coin_id,
                    "price": coin_data.get("usd"),
                    "market_cap": coin_data.get("usd_market_cap"),
                    "volume_24h": coin_data.get("usd_24h_vol"),
                    "change_24h": coin_data.get("usd_24h_change"),
                    "timestamp": datetime.utcnow().isoformat()
                }

        else:
            print("CoinGecko failed:", res.status_code)

    except Exception as e:
        print("CoinGecko error:", e)

    # =========================
    # 2️⃣ CoinCap (Fallback)
    # =========================
    for coin_id in ids:
        if coin_id in results:
            continue

        try:
            url = f"https://api.coincap.io/v2/assets/{coin_id}"

            async with httpx.AsyncClient(timeout=10) as client:
                res = await client.get(url)

            if res.status_code == 200:
                data = res.json().get("data", {})

                results[coin_id] = {
                    "symbol": coin_id,
                    "price": float(data.get("priceUsd", 0)),
                    "market_cap": float(data.get("marketCapUsd", 0)),
                    "volume_24h": float(data.get("volumeUsd24Hr", 0)),
                    "change_24h": float(data.get("changePercent24Hr", 0)),
                    "timestamp": datetime.utcnow().isoformat()
                }

                print(f"CoinCap fallback used for {coin_id}")

        except Exception as e:
            print(f"CoinCap failed for {coin_id}:", e)

    return results


@celery_app.task(bind=True, max_retries=3)
def fetch_and_cache_prices(self, symbols: list):

    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        async def run():
            await cache.init()

            ids = [coin.lower() for coin in symbols]

            if not ids:
                print("No valid symbols")
                return

            # 🔥 Fetch from providers
            data = await fetch_prices(ids)

            if not data:
                print("No data fetched from any provider")
                return

            # 🔥 Save to Redis
            for coin_id, price_data in data.items():

                await cache.set(
                    f"crypto_price:{coin_id}",
                    price_data,
                    ttl=600
                )

                await cache.publish(
                    f"price_updates:{coin_id}",
                    json.dumps(price_data)
                )

                print(f"Updated {coin_id}: ${price_data['price']}")

            await cache.close()

        loop.run_until_complete(run())

    except Exception as e:
        print("Price update failed:", e)
        raise self.retry(countdown=60)

    return {"status": "completed"}