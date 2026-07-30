import logging
import os
from datetime import datetime
from typing import Optional
from pathlib import Path


class ProjectLogger:
    """Centralized logging configuration for the AI Job Agent project."""
    
    def __init__(
        self,
        name: str = "ai_job_agent",
        log_level: str = "INFO",
        log_dir: str = "logs"
    ):
        self.name = name
        self.log_level = getattr(logging, log_level.upper())
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        self.logger = self._setup_logger()
    
    def _setup_logger(self) -> logging.Logger:
        """Configure and return the logger instance."""
        logger = logging.getLogger(self.name)
        logger.setLevel(self.log_level)
        
        # Remove existing handlers to avoid duplicates
        logger.handlers.clear()
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.log_level)
        console_formatter = self._get_formatter(use_colors=True)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        
        # File handler
        log_file = self.log_dir / f"{self.name}_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(self.log_level)
        file_formatter = self._get_formatter(use_colors=False)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        
        return logger
    
    def _get_formatter(self, use_colors: bool = False) -> logging.Formatter:
        """Create log formatter with optional color support."""
        if use_colors:
            # ANSI color codes
            COLORS = {
                'DEBUG': '\033[36m',      # Cyan
                'INFO': '\033[32m',       # Green
                'WARNING': '\033[33m',    # Yellow
                'ERROR': '\033[31m',     # Red
                'CRITICAL': '\033[35m',  # Magenta
                'RESET': '\033[0m'
            }
            
            class ColoredFormatter(logging.Formatter):
                def format(self, record):
                    level_color = COLORS.get(record.levelname, COLORS['RESET'])
                    record.levelname = f"{level_color}{record.levelname}{COLORS['RESET']}"
                    return super().format(record)
            
            formatter = ColoredFormatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
        else:
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
        
        return formatter
    
    def get_logger(self) -> logging.Logger:
        """Return the configured logger instance."""
        return self.logger


def get_logger(name: str = "ai_job_agent", log_level: str = "INFO") -> logging.Logger:
    """
    Convenience function to get a configured logger.
    
    Args:
        name: Logger name
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Returns:
        Configured logger instance
    """
    project_logger = ProjectLogger(name=name, log_level=log_level)
    return project_logger.get_logger()


# Example usage
if __name__ == "__main__":
    logger = get_logger()
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
