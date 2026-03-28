"""Main FastAPI application entry point."""
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.logger import logger, setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager."""
    # Startup
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    yield
    # Shutdown
    logger.info("Shutting down application...")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="A modern Kanban board API with user authentication and real-time collaboration.",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# Exception handlers
# ============================================================================


@app.exception_handler(HTTPException)
async def http_exception_handler(
    request: Request,
    exc: HTTPException,
) -> JSONResponse:
    """Handle HTTP exceptions with a standardized error response."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": f"HTTP_{exc.status_code}",
                "message": exc.detail,
            },
            "details": None,
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    """Handle validation errors with a standardized error response."""
    errors = []
    for error in exc.errors():
        errors.append(
            {
                "field": ".".join(str(loc) for loc in error["loc"] if loc != "body"),
                "message": error["msg"],
                "type": error["type"],
            }
        )

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "success": False,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Request validation failed",
                "details": errors,
            },
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle all other exceptions."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred",
            },
            "details": {"message": str(exc)} if settings.DEBUG else None,
        },
    )


# ============================================================================
# WebSocket connection manager
# ============================================================================


class ConnectionManager:
    """
    Manage WebSocket connections for real-time updates.

    This allows pushing updates to connected clients when
    resources like cards, lists, or boards are modified.
    """

    def __init__(self) -> None:
        """Initialize the connection manager."""
        self.active_connections: dict[str, set[Any]] = {}

    async def connect(self, board_id: str, websocket: Any) -> None:
        """
        Connect a client to a board's WebSocket channel.

        Args:
            board_id: The board ID to subscribe to
            websocket: The WebSocket connection
        """
        if board_id not in self.active_connections:
            self.active_connections[board_id] = set()
        self.active_connections[board_id].add(websocket)
        logger.debug(f"Client connected to board {board_id}")

    def disconnect(self, board_id: str, websocket: Any) -> None:
        """
        Disconnect a client from a board's WebSocket channel.

        Args:
            board_id: The board ID to unsubscribe from
            websocket: The WebSocket connection
        """
        if board_id in self.active_connections:
            self.active_connections[board_id].discard(websocket)
            if not self.active_connections[board_id]:
                del self.active_connections[board_id]
            logger.debug(f"Client disconnected from board {board_id}")

    async def broadcast(self, board_id: str, message: dict[str, Any]) -> None:
        """
        Broadcast a message to all clients subscribed to a board.

        Args:
            board_id: The board ID to broadcast to
            message: The message to broadcast
        """
        if board_id in self.active_connections:
            disconnected = set()
            for connection in self.active_connections[board_id]:
                try:
                    await connection.send_json(message)
                except Exception:
                    disconnected.add(connection)

            # Clean up disconnected clients
            for conn in disconnected:
                self.disconnect(board_id, conn)


# Global connection manager instance
manager = ConnectionManager()


# Health check endpoint
@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy", "version": settings.APP_VERSION}


# Root endpoint
@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint with API information."""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",
    }


# API routes
from app.api.endpoints import auth, boards, lists, cards, labels, comments, activities

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(comments.router, prefix="/api", tags=["Comments"])
app.include_router(boards.router, prefix="/api/boards", tags=["Boards"])
app.include_router(lists.router, prefix="/api/lists", tags=["Lists"])
app.include_router(cards.router, prefix="/api/cards", tags=["Cards"])
app.include_router(labels.router, prefix="/api", tags=["Labels"])
app.include_router(activities.router, prefix="/api", tags=["Activities"])
