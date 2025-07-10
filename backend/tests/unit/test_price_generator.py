import pytest
from unittest.mock import MagicMock, patch
from backend.src.services.price_generator import PriceGenerator
from backend.src.repositories.price_repository import AsyncRWLockPriceRepository
from backend.src.domain.entities.ticker import Ticker
from backend.src.core.config import Settings


@pytest.fixture
def mock_settings():
    return Settings(
        ticker_count=3,
        price_update_interval=0.1,
        price_change_range=1.0,
        initial_price_min=50.0,
        initial_price_max=100.0
    )


@pytest.fixture
def price_repository():
    return AsyncRWLockPriceRepository()


@pytest.fixture
def price_generator(price_repository, mock_settings):
    with patch('backend.src.services.price_generator.get_settings', return_value=mock_settings):
        return PriceGenerator(price_repository)


class TestPriceGenerator:
    @pytest.mark.asyncio
    async def test_initialize_tickers(self, price_generator, mock_settings):
        """Test ticker initialization."""
        tickers = await price_generator.initialize_tickers()

        assert len(tickers) == mock_settings.ticker_count

        for i, ticker in enumerate(tickers):
            assert ticker.id == f"ITEM_{i:02d}"
            assert ticker.name == f"Item {i:02d}"
            assert mock_settings.initial_price_min <= ticker.initial_price <= mock_settings.initial_price_max
            assert ticker.current_price == ticker.initial_price

    @pytest.mark.asyncio
    async def test_get_tickers(self, price_generator):
        """Test getting all tickers."""
        await price_generator.initialize_tickers()
        tickers = price_generator.get_tickers()

        assert len(tickers) == 3
        assert all(isinstance(ticker, Ticker) for ticker in tickers)

    @pytest.mark.asyncio
    async def test_get_ticker(self, price_generator):
        """Test getting a specific ticker."""
        await price_generator.initialize_tickers()

        ticker = price_generator.get_ticker("ITEM_00")
        assert ticker is not None
        assert ticker.id == "ITEM_00"

        ticker = price_generator.get_ticker("INVALID")
        assert ticker is None

    @pytest.mark.asyncio
    async def test_start_stop(self, price_generator):
        """Test starting and stopping the price generator."""
        await price_generator.initialize_tickers()

        await price_generator.start()
        assert price_generator._running is True
        assert price_generator._task is not None

        await price_generator.stop()
        assert price_generator._running is False

    @pytest.mark.asyncio
    async def test_price_updates(self, price_generator, price_repository):
        """Test that prices are updated."""
        await price_generator.initialize_tickers()

        initial_prices = {
            ticker.id: ticker.current_price
            for ticker in price_generator.get_tickers()
        }

        await price_generator._update_all_prices()

        updated_tickers = price_generator.get_tickers()
        price_changed = False

        for ticker in updated_tickers:
            if ticker.current_price != initial_prices[ticker.id]:
                price_changed = True
                break

        assert price_changed, "At least one price should have changed"

        for ticker in updated_tickers:
            history = await price_repository.get_history(ticker.id)
            assert len(history) >= 2