"""Main Instagram scraper class"""

import asyncio
from typing import List, Dict, Optional
import pandas as pd
from pathlib import Path

from .config import Config
from .playwright_login import PlaywrightLogin
from .parser import InstagramParser
from .rate_limiter import RateLimiter
from .log import get_logger

logger = get_logger(__name__)


class InstagramScraper:
    """Main Instagram scraper class"""
    
    def __init__(self, config: Config):
        """Initialize Instagram scraper
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.login_handler = PlaywrightLogin(
            config.username,
            config.password,
            config.headless
        )
        self.parser = InstagramParser()
        self.rate_limiter = RateLimiter(
            config.rate_limit_requests,
            config.rate_limit_period
        )
        self.data: List[Dict] = []
        
        logger.info("Instagram scraper initialized")
    
    async def login(self) -> bool:
        """Login to Instagram
        
        Returns:
            True if login successful, False otherwise
        """
        try:
            success = await self.login_handler.login()
            if success:
                logger.info("Successfully logged in to Instagram")
            else:
                logger.error("Failed to login to Instagram")
            return success
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            return False
    
    async def scrape_profile(self, username: str) -> Optional[Dict]:
        """Scrape a user profile
        
        Args:
            username: Instagram username to scrape
            
        Returns:
            Dictionary containing profile data, or None if failed
        """
        try:
            # Rate limiting
            self.rate_limiter.request()
            
            logger.info(f"Scraping profile: {username}")
            
            if not self.login_handler.page:
                logger.error("Not logged in")
                return None
            
            # Navigate to profile
            await self.login_handler.page.goto(
                f"https://www.instagram.com/{username}/",
                timeout=self.config.browser_timeout
            )
            await asyncio.sleep(2)
            
            # Get page content
            html = await self.login_handler.page.content()
            
            # Parse profile info
            profile_data = self.parser.extract_profile_info(html)
            
            return profile_data
            
        except Exception as e:
            logger.error(f"Error scraping profile {username}: {str(e)}")
            return None
    
    async def scrape_profiles_from_file(self, input_file: Optional[str] = None) -> List[Dict]:
        """Scrape multiple profiles from input file
        
        Args:
            input_file: Path to input CSV file. If None, uses config value
            
        Returns:
            List of profile data dictionaries
        """
        if input_file is None:
            input_file = self.config.input_file
        
        try:
            # Read input file
            input_path = Path(input_file)
            if not input_path.exists():
                logger.error(f"Input file not found: {input_file}")
                return []
            
            df = pd.read_csv(input_file)
            if 'username' not in df.columns:
                logger.error("Input file must have 'username' column")
                return []
            
            usernames = df['username'].tolist()
            logger.info(f"Found {len(usernames)} usernames to scrape")
            
            # Login first
            if not await self.login():
                return []
            
            # Scrape each profile
            results = []
            for username in usernames:
                profile_data = await self.scrape_profile(username)
                if profile_data:
                    results.append(profile_data)
            
            self.data = results
            logger.info(f"Successfully scraped {len(results)} profiles")
            
            return results
            
        except Exception as e:
            logger.error(f"Error scraping from file: {str(e)}")
            return []
    
    def save_to_csv(self, output_file: Optional[str] = None):
        """Save scraped data to CSV file
        
        Args:
            output_file: Path to output CSV file. If None, uses config value
        """
        if output_file is None:
            output_file = self.config.output_file
        
        try:
            if not self.data:
                logger.warning("No data to save")
                return
            
            # Create output directory if needed
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Save to CSV
            df = pd.DataFrame(self.data)
            df.to_csv(output_file, index=False)
            
            logger.info(f"Data saved to {output_file}")
            
        except Exception as e:
            logger.error(f"Error saving to CSV: {str(e)}")
    
    async def close(self):
        """Close scraper and cleanup resources"""
        await self.login_handler.close()
        logger.info("Scraper closed")
