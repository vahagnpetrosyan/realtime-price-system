import logging
import sys
from typing import Optional
from .config import get_settings


def setup_logging(log_level: Optional[str] = None) -> None:
    """Configure logging for the application."""
    settings = get_settings()
    level = log_level or settings.log_level

    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("watchfiles").setLevel(logging.WARNING)