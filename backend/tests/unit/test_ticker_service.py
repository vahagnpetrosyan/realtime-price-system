import pytest
from unittest.mock import AsyncMock
from datetime import datetime

from backend.src.services.ticker_service import TickerService
from backend.src.services.price_generator import PriceGenerator
from backend.src.repositories.price_repository import AsyncRWLockPriceRepository
from backend.src.domain.entities.ticker import Ticker
from backend.src.domain.entities.price import Price


@pytest.fixture
def mock_ticker() -> Ticker:
    now = datetime.utcnow()
    return Ticker(
        id="TEST_01",
        name="Test Item 01",
        initial_price=100.0,
        current_price=105.5,
        created_at=now,
        updated_at=now,
    )


@pytest.fixture
def mock_price_generator(mock_ticker) -> PriceGenerator:      # type: ignore[override]
    gen = AsyncMock(spec=PriceGenerator)
    gen.get_tickers.return_value = [mock_ticker]          # awaits → list[Ticker]
    gen.get_ticker.return_value = mock_ticker             # awaits → Ticker | None
    return gen


@pytest.fixture
def mock_price_repository() -> AsyncRWLockPriceRepository:    # type: ignore[override]
    repo = AsyncMock(spec=AsyncRWLockPriceRepository)
    repo.get_history.return_value = [
        Price(ticker_id="TEST_01", value=100.0, timestamp=datetime.utcnow()),
        Price(ticker_id="TEST_01", value=101.5, timestamp=datetime.utcnow()),
        Price(ticker_id="TEST_01", value=105.5, timestamp=datetime.utcnow()),
    ]                                                         # awaits → list[Price]
    return repo


@pytest.fixture
def ticker_service(
    mock_price_generator: PriceGenerator,
    mock_price_repository: AsyncRWLockPriceRepository,
) -> TickerService:
    return TickerService(mock_price_generator, mock_price_repository)


class TestTickerService:

    def test_get_all_tickers(self, ticker_service: TickerService, mock_ticker: Ticker):
        """Ensure `get_all_tickers` returns a normalised list."""
        tickers = ticker_service.get_all_tickers()

        assert len(tickers) == 1
        assert tickers[0]["id"] == mock_ticker.id
        assert tickers[0]["name"] == mock_ticker.name
        assert tickers[0]["current_price"] == round(mock_ticker.current_price, 2)

    @pytest.mark.asyncio
    async def test_get_ticker_history(self, ticker_service: TickerService):
        """Ensure full history is returned for an existing ticker."""
        result = await ticker_service.get_ticker_history("TEST_01")

        assert result["ticker"]["id"] == "TEST_01"
        assert len(result["history"]) == 3
        assert all("value" in p and "timestamp" in p for p in result["history"])

    @pytest.mark.asyncio
    async def test_get_ticker_history_not_found(
        self,
        ticker_service: TickerService,
        mock_price_generator: PriceGenerator,
    ):
        """Raises if ticker is missing."""
        mock_price_generator.get_ticker.return_value = None

        with pytest.raises(ValueError, match="Ticker INVALID not found"):
            await ticker_service.get_ticker_history("INVALID")

    def test_ticker_to_dict(self, ticker_service: TickerService, mock_ticker: Ticker):
        result = ticker_service._ticker_to_dict(mock_ticker)

        assert result["id"] == mock_ticker.id
        assert result["name"] == mock_ticker.name
        assert result["current_price"] == round(mock_ticker.current_price, 2)
        assert result["initial_price"] == round(mock_ticker.initial_price, 2)
        assert "created_at" in result and "updated_at" in result

    def test_price_to_dict(self, ticker_service: TickerService):
        price = Price(ticker_id="TEST_01", value=123.456, timestamp=datetime.utcnow())
        result = ticker_service._price_to_dict(price)

        assert result["value"] == 123.46
        assert "timestamp" in result
