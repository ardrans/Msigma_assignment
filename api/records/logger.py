"""
Centralized logging utility for the batch_processor application.

Usage:
    from records.logger import logger
    
    logger.info("Processing record")
    logger.error("Failed to process", exc_info=True)
    logger.debug("Debug info", extra={"record_id": 123})
"""

import logging
import os
from datetime import datetime
from pathlib import Path

# Create logs directory if it doesn't exist
LOGS_DIR = Path(__file__).resolve().parent.parent / 'logs'
LOGS_DIR.mkdir(exist_ok=True)

# Log file path with date
LOG_FILE = LOGS_DIR / f"app_{datetime.now().strftime('%Y-%m-%d')}.log"


class CustomFormatter(logging.Formatter):
    """Custom formatter with colors for console output."""
    
    COLORS = {
        'DEBUG': '\033[36m',     # Cyan
        'INFO': '\033[32m',      # Green
        'WARNING': '\033[33m',   # Yellow
        'ERROR': '\033[31m',     # Red
        'CRITICAL': '\033[35m',  # Magenta
    }
    RESET = '\033[0m'
    
    def __init__(self, use_colors=True):
        super().__init__()
        self.use_colors = use_colors
        self.fmt = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
        self.datefmt = "%Y-%m-%d %H:%M:%S"
    
    def format(self, record):
        # Create formatter for this record
        if self.use_colors:
            color = self.COLORS.get(record.levelname, self.RESET)
            formatter = logging.Formatter(
                f"{color}{self.fmt}{self.RESET}",
                datefmt=self.datefmt
            )
        else:
            formatter = logging.Formatter(self.fmt, datefmt=self.datefmt)
        
        return formatter.format(record)


def setup_logger(name: str = "batch_processor", level: str = "DEBUG") -> logging.Logger:
    """
    Set up and return a configured logger instance.
    
    Args:
        name: Logger name (default: 'batch_processor')
        level: Logging level (default: 'DEBUG')
    
    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper(), logging.DEBUG))
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    # Console handler with colors
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(CustomFormatter(use_colors=True))
    
    # File handler without colors
    file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(CustomFormatter(use_colors=False))
    
    # Add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger


# Default logger instance - import this
logger = setup_logger()
