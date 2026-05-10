import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from rich.logging import RichHandler

def setup_logger(name: str = "qa_lab", log_level: str = "INFO"):
    """Setup logger with console and file handlers"""
    
    # Create logs directory
    Path("logs").mkdir(exist_ok=True)
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Console handler with rich formatting
    console_handler = RichHandler(
        rich_tracebacks=True,
        markup=True,
        show_time=True,
        show_path=False
    )
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter('%(message)s')
    console_handler.setFormatter(console_format)
    
    # File handler with rotation
    file_handler = RotatingFileHandler(
        f"logs/{name}.log",
        maxBytes=10_000_000,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(file_format)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

# Global logger
logger = setup_logger()
