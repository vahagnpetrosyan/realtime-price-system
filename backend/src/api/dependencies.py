from functools import lru_cache
from backend.src.repositories.price_repository import AsyncRWLockPriceRepository, PriceRepositoryProtocol
from backend.src.services.price_generator import PriceGenerator
from backend.src.services.ticker_service import TickerService


@lru_cache()
def get_price_repository() -> PriceRepositoryProtocol:
    """Get price repository instance."""
    return AsyncRWLockPriceRepository()


@lru_cache()
def get_price_generator() -> PriceGenerator:
    """Get price generator instance."""
    return PriceGenerator(get_price_repository())


@lru_cache()
def get_ticker_service() -> TickerService:
    """Get ticker service instance."""
    return TickerService(get_price_generator(), get_price_repository())