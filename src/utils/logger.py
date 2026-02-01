"""
Centralized logging system for Windows Repair Toolkit.
Provides structured logging with file and console output.
"""

import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Optional


class Logger:
    """Thread-safe singleton logger with file and console handlers."""
    
    _instance: Optional['Logger'] = None
    _initialized: bool = False
    
    def __new__(cls) -> 'Logger':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self) -> None:
        if Logger._initialized:
            return
        
        Logger._initialized = True
        self._setup_logger()
    
    def _setup_logger(self) -> None:
        """Initialize logging configuration."""
        self._logger = logging.getLogger('WinRepairToolkit')
        self._logger.setLevel(logging.DEBUG)
        self._logger.handlers.clear()
        
        log_dir = Path(__file__).parent.parent.parent / 'logs'
        log_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = log_dir / f'toolkit_{timestamp}.log'
        
        file_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(file_formatter)
        
        console_formatter = logging.Formatter(
            '%(levelname)-8s | %(message)s'
        )
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(console_formatter)
        
        self._logger.addHandler(file_handler)
        self._logger.addHandler(console_handler)
        
        self._log_file = log_file
    
    @property
    def log_file(self) -> Path:
        """Return the current log file path."""
        return self._log_file
    
    def info(self, message: str) -> None:
        """Log info level message."""
        self._logger.info(message)
    
    def warning(self, message: str) -> None:
        """Log warning level message."""
        self._logger.warning(message)
    
    def error(self, message: str) -> None:
        """Log error level message."""
        self._logger.error(message)
    
    def debug(self, message: str) -> None:
        """Log debug level message."""
        self._logger.debug(message)
    
    def exception(self, message: str) -> None:
        """Log exception with traceback."""
        self._logger.exception(message)


def get_logger() -> Logger:
    """Get the singleton logger instance."""
    return Logger()
