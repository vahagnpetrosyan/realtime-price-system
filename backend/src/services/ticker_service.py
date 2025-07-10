from typing import List, Optional, Dict, Any
from backend.src.repositories.price_repository import PriceRepositoryProtocol
from backend.src.services.price_generator import PriceGenerator
from backend.src.domain.entities.ticker import Ticker
from backend.src.domain.entities.price import Price


class TickerService:
    """Service for managing tickers and their data."""

    def __init__(self, price_generator: PriceGenerator, price_repository: PriceRepositoryProtocol):
        self.price_generator = price_generator
        self.price_repository = price_repository

    def get_all_tickers(self) -> List[Dict[str, Any]]:
        """Get all available tickers."""
        tickers = self.price_generator.get_tickers()
        return [self._ticker_to_dict(ticker) for ticker in tickers]

    async def get_ticker_history(self, ticker_id: str, limit: Optional[int] = None) -> Dict[str, Any]:
        """Get ticker information with price history."""
        ticker = self.price_generator.get_ticker(ticker_id)
        if not ticker:
            raise ValueError(f"Ticker {ticker_id} not found")

        history = await self.price_repository.get_history(ticker_id, limit)

        return {
            "ticker": self._ticker_to_dict(ticker),
            "history": [self._price_to_dict(price) for price in history]
        }

    def _ticker_to_dict(self, ticker: Ticker) -> Dict[str, Any]:
        """Convert ticker entity to dictionary."""
        return {
            "id": ticker.id,
            "name": ticker.name,
            "current_price": round(ticker.current_price, 2),
            "initial_price": round(ticker.initial_price, 2),
            "created_at": ticker.created_at.isoformat(),
            "updated_at": ticker.updated_at.isoformat()
        }

    def _price_to_dict(self, price: Price) -> Dict[str, Any]:
        """Convert price entity to dictionary."""
        return {
            "value": round(price.value, 2),
            "timestamp": price.timestamp.isoformat()
        }