from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from backend.src.api.dependencies import get_ticker_service
from backend.src.services.ticker_service import TickerService


router = APIRouter(prefix="/tickers", tags=["tickers"])


@router.get("")
async def get_tickers(
    ticker_service: TickerService = Depends(get_ticker_service)
) -> List[dict]:
    """Get list of all available tickers."""
    return ticker_service.get_all_tickers()


@router.get("/{ticker_id}/history")
async def get_ticker_history(
    ticker_id: str,
    limit: Optional[int] = Query(None, ge=1, le=1000),
    ticker_service: TickerService = Depends(get_ticker_service)
) -> dict:
    """Get historical data for a specific ticker."""
    try:
        return await ticker_service.get_ticker_history(ticker_id, limit)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))