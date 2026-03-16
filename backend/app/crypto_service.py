import httpx
from typing import Optional, List
from app.cache import cache

COINGECKO_API_URL = "https://api.coingecko.com/api/v3"


class CryptoService:

    @staticmethod
    async def get_coin_id(symbol: str) -> Optional[str]:
        """
        Resolve symbol -> CoinGecko coin id using cached /coins/list
        """

        symbol = symbol.lower()

        coin_map = await cache.get("coingecko_coin_map")

        if not coin_map:
            await CryptoService.refresh_coin_list()
            coin_map = await cache.get("coingecko_coin_map")

        return coin_map.get(symbol)


    @staticmethod
    async def refresh_coin_list():
        """
        Fetch full coin list from CoinGecko and cache it
        """

        url = f"{COINGECKO_API_URL}/coins/list"

        async with httpx.AsyncClient(timeout=20) as client:
            r = await client.get(url)

        if r.status_code != 200:
            print("Failed to fetch coin list")
            return

        coins = r.json()

        coin_map = {}

        for coin in coins:
            coin_map[coin["symbol"].lower()] = coin["id"]

        await cache.set("coingecko_coin_map", coin_map, ttl=86400)

        print(f"Cached {len(coin_map)} CoinGecko symbols")


    @staticmethod
    async def get_price(symbol: str) -> Optional[dict]:

        price = await cache.get(f"crypto_price:{symbol}")

        if price:
            return price

        from app.tasks import fetch_and_cache_prices
        fetch_and_cache_prices.delay([symbol])

        return None


    @staticmethod
    async def get_prices_bulk(symbols: List[str]) -> dict:

        results = {}

        for symbol in symbols:

            price = await cache.get(f"crypto_price:{symbol}")

            if not price:
                from app.tasks import fetch_and_cache_prices
                fetch_and_cache_prices.delay([symbol])

            results[symbol] = price

        return results


    @staticmethod
    def trigger_price_update(symbols: List[str]):

        from app.tasks import fetch_and_cache_prices
        fetch_and_cache_prices.delay(symbols)