import logging
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.src.core.config import get_settings
from backend.src.core.logging import setup_logging
from backend.src.core.events import event_bus
from backend.src.api.routes import ticker_routes, websocket_routes
from backend.src.api.dependencies import get_price_generator
from backend.src.services.websocket_manager import websocket_manager

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    setup_logging()

    logger.info("Starting Real-Time Price Data System")

    # Initialize and start price generator
    price_generator = get_price_generator()
    await price_generator.initialize_tickers()

    # Subscribe WebSocket manager to price updates
    async def handle_price_update(event):
        await websocket_manager.broadcast_price_update(event)

    event_bus.subscribe("price_update", handle_price_update)

    # Start price generation
    await price_generator.start()

    yield

    # Shutdown
    logger.info("Shutting down Real-Time Price Data System")
    await price_generator.stop()
    event_bus.unsubscribe("price_update", handle_price_update)


def create_app() -> FastAPI:
    """Create FastAPI application."""
    settings = get_settings()

    app = FastAPI(
        title=settings.api_title,
        version=settings.api_version,
        lifespan=lifespan
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(
        ticker_routes.router,
        prefix=settings.api_prefix
    )
    app.include_router(websocket_routes.router)

    @app.get("/health")
    async def health_check():
        """Health check endpoint."""
        return {"status": "healthy"}

    return app


app = create_app()

if __name__ == "__main__":

    settings = get_settings()

    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload
    )