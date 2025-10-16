"""Instagram scraper main module."""

import asyncio
from pathlib import Path
from typing import List, Dict, Any, Optional
import pandas as pd

from .config import Config
from .playwright_login import PlaywrightLogin
from .parser import InstagramParser
from .rate_limiter import RateLimiter
from .log import setup_logger, get_logger


class InstagramScraper:
    """Main Instagram scraper class."""

    def __init__(self, config: Config, headless: bool = True):
        """Initialize Instagram scraper.
        
        Args:
            config: Configuration object
            headless: Run browser in headless mode
        """
        self.config = config
        self.headless = headless
        self.logger = setup_logger(level=config.log_level)
        self.rate_limiter = RateLimiter(
            max_requests=config.rate_limit_requests,
            time_period=config.rate_limit_period
        )
        self.parser = InstagramParser()
        self.login_handler: Optional[PlaywrightLogin] = None

    async def initialize(self):
        """Initialize the scraper and login."""
        self.logger.info("Initializing Instagram scraper...")
        
        # Validate configuration
        if not self.config.validate():
            raise ValueError("Invalid configuration: username and password required")
        
        # Create user data directory for session persistence
        user_data_dir = Path("./browser_data")
        
        # Initialize login handler
        self.login_handler = PlaywrightLogin(
            headless=self.headless,
            user_data_dir=user_data_dir
        )
        await self.login_handler.start()
        
        # Login to Instagram
        success = await self.login_handler.login(
            self.config.ig_username,
            self.config.ig_password
        )
        
        if not success:
            raise RuntimeError("Failed to login to Instagram")
        
        self.logger.info("Scraper initialized successfully")

    async def scrape_user_profile(self, username: str) -> Dict[str, Any]:
        """Scrape user profile information.
        
        Args:
            username: Instagram username to scrape
            
        Returns:
            Dictionary containing user profile data
        """
        self.logger.info(f"Scraping profile: {username}")
        
        # Rate limiting
        self.rate_limiter.acquire()
        
        # Get page content
        url = f"https://www.instagram.com/{username}/"
        html = await self.login_handler.get_page_content(url)
        
        # Parse profile data
        profile_data = self.parser.parse_user_profile(html)
        profile_data['username'] = username
        
        self.logger.info(f"Profile scraped: {username}")
        return profile_data

    async def scrape_users(self, usernames: List[str]) -> List[Dict[str, Any]]:
        """Scrape multiple user profiles.
        
        Args:
            usernames: List of Instagram usernames to scrape
            
        Returns:
            List of dictionaries containing user profile data
        """
        self.logger.info(f"Scraping {len(usernames)} profiles...")
        
        results = []
        for username in usernames:
            try:
                profile_data = await self.scrape_user_profile(username)
                results.append(profile_data)
            except Exception as e:
                self.logger.error(f"Error scraping {username}: {str(e)}")
                results.append({
                    'username': username,
                    'error': str(e)
                })
        
        self.logger.info(f"Scraping completed: {len(results)} profiles")
        return results

    async def close(self):
        """Close the scraper and cleanup resources."""
        self.logger.info("Closing scraper...")
        if self.login_handler:
            await self.login_handler.close()
        self.logger.info("Scraper closed")

    async def __aenter__(self):
        """Async context manager entry."""
        await self.initialize()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()

    def save_results(self, results: List[Dict[str, Any]], output_file: Path):
        """Save scraping results to CSV file.
        
        Args:
            results: List of scraping results
            output_file: Path to output CSV file
        """
        self.logger.info(f"Saving results to {output_file}")
        
        # Create output directory if it doesn't exist
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert to DataFrame and save
        df = pd.DataFrame(results)
        df.to_csv(output_file, index=False)
        
        self.logger.info(f"Results saved: {len(results)} records")

    @staticmethod
    def load_input(input_file: Path) -> List[str]:
        """Load usernames from input CSV file.
        
        Args:
            input_file: Path to input CSV file
            
        Returns:
            List of usernames
        """
        df = pd.read_csv(input_file)
        if 'username' in df.columns:
            return df['username'].tolist()
        elif len(df.columns) > 0:
            return df.iloc[:, 0].tolist()
        else:
            raise ValueError("Invalid input file format")
