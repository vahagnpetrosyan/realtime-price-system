from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any


@dataclass
class PriceUpdateEvent:
    """Event emitted when a price is updated."""

    ticker_id: str
    price: float
    timestamp: datetime

    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary for serialization."""
        return {
            "ticker_id": self.ticker_id,
            "price": self.price,
            "timestamp": self.timestamp.isoformat()
        }