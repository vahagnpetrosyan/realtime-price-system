import asyncio
from typing import Dict, List, Callable, Any
from collections import defaultdict


class EventBus:
    """Simple event bus for internal event handling."""

    def __init__(self):
        self._handlers: Dict[str, List[Callable]] = defaultdict(list)

    def subscribe(self, event_type: str, handler: Callable) -> None:
        """Subscribe to an event type."""
        self._handlers[event_type].append(handler)

    def unsubscribe(self, event_type: str, handler: Callable) -> None:
        """Unsubscribe from an event type."""
        if handler in self._handlers[event_type]:
            self._handlers[event_type].remove(handler)

    async def emit(self, event_type: str, data: Any) -> None:
        """Emit an event to all subscribers."""
        handlers = self._handlers.get(event_type, [])
        if handlers:
            await asyncio.gather(
                *[handler(data) for handler in handlers],
                return_exceptions=True
            )


event_bus = EventBus()