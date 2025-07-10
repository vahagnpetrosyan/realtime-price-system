from typing import List, Dict, Optional, Protocol
from collections import defaultdict, deque
import asyncio
from backend.src.domain.entities.price import Price
from backend.src.core.config import get_settings


class PriceRepositoryProtocol(Protocol):
    """Protocol for price repository implementations."""

    async def add_price(self, price: Price) -> None: ...

    async def get_history(self, ticker_id: str, limit: Optional[int] = None) -> List[Price]: ...

    async def get_latest_price(self, ticker_id: str) -> Optional[Price]: ...

    async def clear_history(self, ticker_id: str) -> None: ...


class AsyncRWLock:
    """Async read-write lock implementation."""

    def __init__(self):
        self._read_count = 0
        self._write_lock = asyncio.Lock()
        self._read_lock = asyncio.Lock()
        self._no_readers = asyncio.Event()
        self._no_readers.set()

    async def acquire_read(self):
        """Acquire read lock."""
        async with self._read_lock:
            self._read_count += 1
            if self._read_count == 1:
                self._no_readers.clear()

    async def release_read(self):
        """Release read lock."""
        async with self._read_lock:
            self._read_count -= 1
            if self._read_count == 0:
                self._no_readers.set()

    async def acquire_write(self):
        """Acquire write lock."""
        await self._write_lock.acquire()
        await self._no_readers.wait()

    def release_write(self):
        """Release write lock."""
        self._write_lock.release()


class AsyncRWLockPriceRepository(PriceRepositoryProtocol):
    """Price repository with async read-write lock for better concurrency."""

    def __init__(self):
        self.settings = get_settings()
        self._history: Dict[str, deque] = defaultdict(
            lambda: deque(maxlen=self.settings.max_history_size)
        )
        self._rw_lock = AsyncRWLock()

    async def add_price(self, price: Price) -> None:
        """Add a new price to the history."""
        await self._rw_lock.acquire_write()
        try:
            self._history[price.ticker_id].append(price)
        finally:
            self._rw_lock.release_write()

    async def get_history(self, ticker_id: str, limit: Optional[int] = None) -> List[Price]:
        """Get price history for a ticker."""
        await self._rw_lock.acquire_read()
        try:
            history = list(self._history.get(ticker_id, []))
            if limit:
                return history[-limit:]
            return history
        finally:
            await self._rw_lock.release_read()

    async def get_latest_price(self, ticker_id: str) -> Optional[Price]:
        """Get the latest price for a ticker."""
        await self._rw_lock.acquire_read()
        try:
            history = self._history.get(ticker_id)
            if history:
                return history[-1]
            return None
        finally:
            await self._rw_lock.release_read()

    async def clear_history(self, ticker_id: str) -> None:
        """Clear history for a specific ticker."""
        await self._rw_lock.acquire_write()
        try:
            if ticker_id in self._history:
                self._history[ticker_id].clear()
        finally:
            self._rw_lock.release_write()
