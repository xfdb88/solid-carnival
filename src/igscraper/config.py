"""Configuration module for Instagram Scraper"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv


class Config:
    """Configuration class for Instagram Scraper"""
    
    def __init__(self, env_file: Optional[str] = None):
        """Initialize configuration from environment variables
        
        Args:
            env_file: Path to .env file. If None, loads from default location
        """
        if env_file:
            load_dotenv(env_file)
        else:
            load_dotenv()
        
        # Instagram credentials
        self.username = os.getenv("INSTAGRAM_USERNAME", "")
        self.password = os.getenv("INSTAGRAM_PASSWORD", "")
        
        # Rate limiting
        self.rate_limit_requests = int(os.getenv("RATE_LIMIT_REQUESTS", "10"))
        self.rate_limit_period = int(os.getenv("RATE_LIMIT_PERIOD", "60"))
        
        # File paths
        self.output_file = os.getenv("OUTPUT_FILE", "data/output.csv")
        self.input_file = os.getenv("INPUT_FILE", "data/input.csv")
        
        # Logging
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.log_file = os.getenv("LOG_FILE", "logs/igscraper.log")
        
        # Browser settings
        self.headless = os.getenv("HEADLESS", "true").lower() == "true"
        self.browser_timeout = int(os.getenv("BROWSER_TIMEOUT", "30000"))
    
    def validate(self) -> bool:
        """Validate configuration settings
        
        Returns:
            True if configuration is valid, False otherwise
        """
        if not self.username or not self.password:
            return False
        
        if self.rate_limit_requests <= 0 or self.rate_limit_period <= 0:
            return False
        
        return True
    
    def __repr__(self) -> str:
        """String representation of Config (hiding password)"""
        return (
            f"Config(username={self.username}, "
            f"rate_limit={self.rate_limit_requests}/{self.rate_limit_period}s, "
            f"headless={self.headless})"
        )
