"""Playwright-based login for Instagram."""

import asyncio
from pathlib import Path
from typing import Optional
from playwright.async_api import async_playwright, Browser, Page, BrowserContext
from .log import get_logger


logger = get_logger(__name__)


class PlaywrightLogin:
    """Handle Instagram login using Playwright."""

    def __init__(self, headless: bool = True, user_data_dir: Optional[Path] = None):
        """Initialize Playwright login handler.
        
        Args:
            headless: Run browser in headless mode
            user_data_dir: Directory to store browser user data for session persistence
        """
        self.headless = headless
        self.user_data_dir = user_data_dir
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self._playwright = None

    async def start(self):
        """Start the browser."""
        logger.info("Starting browser...")
        self._playwright = await async_playwright().start()
        
        if self.user_data_dir:
            self.user_data_dir.mkdir(parents=True, exist_ok=True)
            self.context = await self._playwright.chromium.launch_persistent_context(
                str(self.user_data_dir),
                headless=self.headless,
                viewport={'width': 1280, 'height': 720},
            )
            self.page = self.context.pages[0] if self.context.pages else await self.context.new_page()
        else:
            self.browser = await self._playwright.chromium.launch(headless=self.headless)
            self.context = await self.browser.new_context(
                viewport={'width': 1280, 'height': 720},
            )
            self.page = await self.context.new_page()
        
        logger.info("Browser started successfully")

    async def login(self, username: str, password: str) -> bool:
        """Login to Instagram.
        
        Args:
            username: Instagram username
            password: Instagram password
            
        Returns:
            True if login successful, False otherwise
        """
        try:
            logger.info(f"Logging in as {username}...")
            
            # Navigate to Instagram login page
            await self.page.goto("https://www.instagram.com/accounts/login/")
            await asyncio.sleep(2)
            
            # Accept cookies if present
            try:
                accept_button = await self.page.wait_for_selector(
                    'button:has-text("Accept")', timeout=3000
                )
                if accept_button:
                    await accept_button.click()
                    await asyncio.sleep(1)
            except Exception:
                pass  # No cookie banner
            
            # Fill in username
            await self.page.fill('input[name="username"]', username)
            await asyncio.sleep(0.5)
            
            # Fill in password
            await self.page.fill('input[name="password"]', password)
            await asyncio.sleep(0.5)
            
            # Click login button
            await self.page.click('button[type="submit"]')
            
            # Wait for navigation
            await asyncio.sleep(5)
            
            # Check if login was successful
            current_url = self.page.url
            if "accounts/login" not in current_url:
                logger.info("Login successful")
                
                # Handle "Save Your Login Info" prompt
                try:
                    not_now_button = await self.page.wait_for_selector(
                        'button:has-text("Not Now")', timeout=3000
                    )
                    if not_now_button:
                        await not_now_button.click()
                        await asyncio.sleep(1)
                except Exception:
                    pass
                
                # Handle "Turn on Notifications" prompt
                try:
                    not_now_button = await self.page.wait_for_selector(
                        'button:has-text("Not Now")', timeout=3000
                    )
                    if not_now_button:
                        await not_now_button.click()
                        await asyncio.sleep(1)
                except Exception:
                    pass
                
                return True
            else:
                logger.error("Login failed")
                return False
                
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            return False

    async def get_page_content(self, url: str) -> str:
        """Navigate to URL and get page content.
        
        Args:
            url: URL to navigate to
            
        Returns:
            HTML content of the page
        """
        logger.info(f"Navigating to {url}")
        await self.page.goto(url)
        await asyncio.sleep(2)
        return await self.page.content()

    async def close(self):
        """Close the browser."""
        logger.info("Closing browser...")
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self._playwright:
            await self._playwright.stop()
        logger.info("Browser closed")

    async def __aenter__(self):
        """Async context manager entry."""
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
