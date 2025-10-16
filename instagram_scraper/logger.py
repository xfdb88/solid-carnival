"""Logging configuration for Instagram scraper."""

import logging
import sys
from datetime import datetime
from pathlib import Path
from instagram_scraper.config import Config

def setup_logger(name: str = "instagram_scraper") -> logging.Logger:
    """Setup and configure logger."""
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, Config.LOG_LEVEL))
    
    if logger.handlers:
        return logger
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    log_file = Config.LOGS_DIR / f"scraper_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger
