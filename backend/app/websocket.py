import json
from redis.asyncio import Redis
from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, Set
import os
import asyncio

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}
        self.redis = None

    async def init_redis(self):
        """Initialize Redis pub/sub connection"""
        self.redis = await Redis.from_url(REDIS_URL, decode_responses=True)

    async def connect(self, websocket: WebSocket, symbol: str):
        """Accept WebSocket connection"""
        await websocket.accept()
        if symbol not in self.active_connections:
            self.active_connections[symbol] = set()
        self.active_connections[symbol].add(websocket)

    async def disconnect(self, websocket: WebSocket, symbol: str):
        """Remove WebSocket connection"""
        if symbol in self.active_connections:
            self.active_connections[symbol].discard(websocket)
            if not self.active_connections[symbol]:
                del self.active_connections[symbol]

    async def broadcast_to_symbol(self, symbol: str, data: str):
        """Broadcast message to all clients subscribed to a symbol"""
        if symbol in self.active_connections:
            disconnected = set()
            for connection in self.active_connections[symbol]:
                try:
                    await connection.send_text(data)
                except Exception:
                    disconnected.add(connection)
            
            # Remove disconnected clients
            for connection in disconnected:
                await self.disconnect(connection, symbol)

    async def subscribe_to_updates(self, symbol: str):
        """Subscribe to Redis pub/sub channel for price updates"""
        if not self.redis:
            await self.init_redis()
        
        try:
            pubsub = self.redis.pubsub()
            await pubsub.subscribe(f"price_updates:{symbol}")
            
            async for message in pubsub.listen():
                if message["type"] == "message":
                    await self.broadcast_to_symbol(
                        symbol,
                        message["data"]
                    )
        except Exception as e:
            print(f"Error in Redis subscription: {e}")


# Global connection manager
manager = ConnectionManager()