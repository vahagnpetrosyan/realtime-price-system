import asyncio
import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from backend.src.services.websocket_manager import websocket_manager
from backend.src.api.dependencies import get_ticker_service
from backend.src.services.ticker_service import TickerService

router = APIRouter(tags=["websocket"])
logger = logging.getLogger(__name__)


@router.websocket("/ws/{ticker_id}")
async def websocket_endpoint(
        websocket: WebSocket,
        ticker_id: str,
        ticker_service: TickerService = Depends(get_ticker_service)
):
    """WebSocket endpoint for real-time price updates."""
    # Validate ticker exists
    try:
        await ticker_service.get_ticker_history(ticker_id, limit=1)
    except ValueError:
        await websocket.close(code=4004, reason="Ticker not found")
        return

    # Connect client
    await websocket_manager.connect(websocket, ticker_id)

    try:
        # Keep connection alive
        while True:
            # Wait for any message from client (ping/pong)
            await websocket.receive_text()
    except WebSocketDisconnect:
        logger.info(f"Client disconnected from ticker {ticker_id}")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        await websocket_manager.disconnect(websocket, ticker_id)