from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings."""

    # API Settings
    api_title: str = "Real-Time Price Data System"
    api_version: str = "1.0.0"
    api_prefix: str = "/api/v1"

    # Server Settings
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = False

    # Price Generation Settings
    ticker_count: int = 10
    price_update_interval: float = 1.0  # seconds
    price_change_range: float = 1.0  # +/- range for price changes
    initial_price_min: float = 50.0
    initial_price_max: float = 200.0
    consecutive_errors: int = 10

    # History Settings
    max_history_size: int = 1000  # per ticker

    # CORS Settings
    cors_origins: list[str] = ["http://localhost:3000", "http://frontend:3000"]

    # Logging
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()