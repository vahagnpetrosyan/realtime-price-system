from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Ticker:
    """Domain entity representing a trading ticker."""

    id: str
    name: str
    initial_price: float
    current_price: float
    created_at: datetime
    updated_at: datetime

    def __post_init__(self):
        if self.initial_price <= 0:
            raise ValueError("Initial price must be positive")
        if self.current_price <= 0:
            raise ValueError("Current price must be positive")

    def update_price(self, new_price: float) -> None:
        """Update the current price of the ticker."""
        if new_price <= 0:
            raise ValueError("Price must be positive")
        self.current_price = new_price
        self.updated_at = datetime.utcnow()