import asyncio
import random
import logging
from datetime import datetime
from typing import Dict, List, Optional
from backend.src.domain.entities.ticker import Ticker
from backend.src.domain.entities.price import Price
from backend.src.domain.events.price_events import PriceUpdateEvent
from backend.src.repositories.price_repository import PriceRepositoryProtocol
from backend.src.core.config import get_settings
from backend.src.core.events import event_bus

logger = logging.getLogger(__name__)


class PriceGenerator:
    """Service for generating random price updates."""

    def __init__(self, price_repository: PriceRepositoryProtocol):
        self.settings = get_settings()
        self.price_repository = price_repository
        self._running = False
        self._task: Optional[asyncio.Task] = None
        self._tickers: Dict[str, Ticker] = {}

    async def initialize_tickers(self) -> List[Ticker]:
        """Initialize tickers with random starting prices."""
        tickers = []

        for i in range(self.settings.ticker_count):
            ticker_id = f"ITEM_{i:02d}"
            initial_price = random.uniform(
                self.settings.initial_price_min,
                self.settings.initial_price_max
            )

            ticker = Ticker(
                id=ticker_id,
                name=f"Item {i:02d}",
                initial_price=initial_price,
                current_price=initial_price,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )

            self._tickers[ticker_id] = ticker
            tickers.append(ticker)

            initial_price_point = Price(
                ticker_id=ticker_id,
                value=initial_price,
                timestamp=datetime.utcnow()
            )
            await self.price_repository.add_price(initial_price_point)

        logger.info(f"Initialized {len(tickers)} tickers")
        return tickers

    async def start(self) -> None:
        """Start generating price updates."""
        if self._running:
            logger.warning("Price generator is already running")
            return

        self._running = True
        self._task = asyncio.create_task(self._generate_prices())
        logger.info("Price generator started")

    async def stop(self) -> None:
        """Stop generating price updates."""
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info("Price generator stopped")

    async def _generate_prices(self) -> None:
        """Generate price updates continuously."""
        while self._running:
            try:
                await self._update_all_prices()
                await asyncio.sleep(self.settings.price_update_interval)
            except Exception as e:
                logger.error(f"Error generating prices: {e}")

    async def _update_all_prices(self) -> None:
        """Update prices for all tickers."""
        for ticker_id, ticker in self._tickers.items():
            change = random.uniform(
                -self.settings.price_change_range,
                self.settings.price_change_range
            )

            new_price = max(0.01, ticker.current_price + change)

            ticker.update_price(new_price)

            price = Price(
                ticker_id=ticker_id,
                value=new_price,
                timestamp=datetime.utcnow()
            )

            await self.price_repository.add_price(price)

            event = PriceUpdateEvent(
                ticker_id=ticker_id,
                price=new_price,
                timestamp=price.timestamp
            )
            await event_bus.emit("price_update", event)

    def get_tickers(self) -> List[Ticker]:
        """Get all tickers."""
        return list(self._tickers.values())

    def get_ticker(self, ticker_id: str) -> Optional[Ticker]:
        """Get a specific ticker."""
        return self._tickers.get(ticker_id)