import asyncio
import json
import logging
from typing import Dict, Set, Optional
from fastapi import WebSocket
from backend.src.core.events import event_bus
from backend.src.domain.events.price_events import PriceUpdateEvent

logger = logging.getLogger(__name__)


class WebSocketManager:
    """Manager for WebSocket connections and broadcasting."""

    def __init__(self):
        # Store active connections by ticker_id
        self._connections: Dict[str, Set[WebSocket]] = {}
        self._lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket, ticker_id: str) -> None:
        """Accept and register a new WebSocket connection."""
        await websocket.accept()

        async with self._lock:
            if ticker_id not in self._connections:
                self._connections[ticker_id] = set()
            self._connections[ticker_id].add(websocket)

        logger.info(f"Client connected to ticker {ticker_id}")

    async def disconnect(self, websocket: WebSocket, ticker_id: str) -> None:
        """Remove a WebSocket connection."""
        async with self._lock:
            if ticker_id in self._connections:
                self._connections[ticker_id].discard(websocket)
                if not self._connections[ticker_id]:
                    del self._connections[ticker_id]

        logger.info(f"Client disconnected from ticker {ticker_id}")

    async def broadcast_price_update(self, event: PriceUpdateEvent) -> None:
        """Broadcast price update to all connected clients for a ticker."""
        ticker_id = event.ticker_id

        async with self._lock:
            connections = self._connections.get(ticker_id, set()).copy()

        if not connections:
            return

        message = json.dumps({
            "type": "price_update",
            "data": event.to_dict()
        })

        # Send to all connections concurrently
        disconnected = []

        async def send_to_client(ws: WebSocket) -> None:
            try:
                await ws.send_text(message)
            except Exception:
                disconnected.append(ws)

        await asyncio.gather(
            *[send_to_client(ws) for ws in connections],
            return_exceptions=True
        )

        # Clean up disconnected clients
        if disconnected:
            async with self._lock:
                for ws in disconnected:
                    self._connections[ticker_id].discard(ws)

    async def send_error(self, websocket: WebSocket, error: str) -> None:
        """Send error message to a specific client."""
        try:
            await websocket.send_text(json.dumps({
                "type": "error",
                "message": error
            }))
        except Exception:
            pass

    def get_connection_count(self, ticker_id: Optional[str] = None) -> int:
        """Get number of active connections."""
        if ticker_id:
            return len(self._connections.get(ticker_id, set()))
        return sum(len(conns) for conns in self._connections.values())


websocket_manager = WebSocketManager()