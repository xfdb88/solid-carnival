"""Configuration management for Instagram scraper."""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration."""
    
    INSTAGRAM_USERNAME = os.getenv("INSTAGRAM_USERNAME", "")
    INSTAGRAM_PASSWORD = os.getenv("INSTAGRAM_PASSWORD", "")
    PROXY_URL = os.getenv("PROXY_URL", "")
    RATE_LIMIT_DELAY = float(os.getenv("RATE_LIMIT_DELAY", "2"))
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
    RETRY_DELAY = int(os.getenv("RETRY_DELAY", "5"))
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / "data"
    LOGS_DIR = BASE_DIR / "logs"
    INPUT_CSV = DATA_DIR / "input.csv"
    OUTPUT_CSV = DATA_DIR / "output.csv"
    
    @classmethod
    def validate(cls):
        """Validate configuration."""
        if not cls.INSTAGRAM_USERNAME or not cls.INSTAGRAM_PASSWORD:
            raise ValueError("Instagram credentials must be set in .env file")
        
        cls.DATA_DIR.mkdir(exist_ok=True)
        cls.LOGS_DIR.mkdir(exist_ok=True)
