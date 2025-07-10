from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Price:
    """Domain entity representing a price point."""

    ticker_id: str
    value: float
    timestamp: datetime
    volume: Optional[float] = None

    def __post_init__(self):
        if self.value <= 0:
            raise ValueError("Price value must be positive")