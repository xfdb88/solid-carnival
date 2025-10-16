"""Configuration management for Instagram scraper."""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv


class Config:
    """Configuration class for Instagram scraper."""

    def __init__(self, env_file: Optional[str] = None):
        """Initialize configuration.
        
        Args:
            env_file: Path to .env file. If None, uses .env in current directory.
        """
        if env_file:
            load_dotenv(env_file)
        else:
            load_dotenv()
        
        # Instagram credentials
        self.ig_username = os.getenv("IG_USERNAME", "")
        self.ig_password = os.getenv("IG_PASSWORD", "")
        
        # Rate limiting settings
        self.rate_limit_requests = int(os.getenv("RATE_LIMIT_REQUESTS", "10"))
        self.rate_limit_period = int(os.getenv("RATE_LIMIT_PERIOD", "60"))
        
        # Output settings
        self.output_dir = Path(os.getenv("OUTPUT_DIR", "data"))
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        
    def validate(self) -> bool:
        """Validate configuration.
        
        Returns:
            True if configuration is valid, False otherwise.
        """
        if not self.ig_username or not self.ig_password:
            return False
        return True
