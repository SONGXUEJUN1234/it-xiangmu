"""Logging configuration for the application."""
import logging
import sys

from loguru import logger as _logger

from .config import settings


class InterceptHandler(logging.Handler):
    """Intercept standard logging messages and redirect to Loguru."""

    def emit(self, record: logging.LogRecord) -> None:
        """Emit a log record to Loguru."""
        # Get corresponding Loguru level if it exists
        try:
            level = _logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        _logger.opt(depth=depth).log(level, record.getMessage())


def setup_logging() -> None:
    """Configure logging for the application."""
    # Intercept standard logging
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

    # Remove default logger and add custom handler
    _logger.remove()
    _logger.add(
        sys.stdout,
        level="DEBUG" if settings.DEBUG else "INFO",
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        colorize=True,
    )


# Get logger instance
logger = _logger
