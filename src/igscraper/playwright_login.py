"""Playwright login handler for Instagram"""

import asyncio
from typing import Optional
from playwright.async_api import Page, Browser, async_playwright
from .log import get_logger

logger = get_logger(__name__)


class PlaywrightLogin:
    """Handle Instagram login using Playwright"""
    
    def __init__(self, username: str, password: str, headless: bool = True):
        """Initialize login handler
        
        Args:
            username: Instagram username
            password: Instagram password
            headless: Whether to run browser in headless mode
        """
        self.username = username
        self.password = password
        self.headless = headless
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
    
    async def start_browser(self) -> Page:
        """Start browser and navigate to Instagram login page
        
        Returns:
            Page object for the Instagram login page
        """
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=self.headless)
        context = await self.browser.new_context()
        self.page = await context.new_page()
        
        logger.info("Browser started successfully")
        await self.page.goto("https://www.instagram.com/accounts/login/")
        await asyncio.sleep(2)
        
        return self.page
    
    async def login(self) -> bool:
        """Perform login to Instagram
        
        Returns:
            True if login successful, False otherwise
        """
        try:
            if not self.page:
                await self.start_browser()
            
            logger.info(f"Attempting to login as {self.username}")
            
            # Wait for login form to load
            await self.page.wait_for_selector('input[name="username"]', timeout=10000)
            
            # Fill in credentials
            await self.page.fill('input[name="username"]', self.username)
            await self.page.fill('input[name="password"]', self.password)
            
            # Click login button
            await self.page.click('button[type="submit"]')
            
            # Wait for navigation or error
            await asyncio.sleep(5)
            
            # Check if login was successful
            current_url = self.page.url
            if "login" not in current_url:
                logger.info("Login successful")
                return True
            else:
                logger.error("Login failed - still on login page")
                return False
                
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            return False
    
    async def close(self):
        """Close browser"""
        if self.browser:
            await self.browser.close()
            logger.info("Browser closed")
