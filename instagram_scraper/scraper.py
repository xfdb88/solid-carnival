"""Instagram profile scraper with Playwright and httpx."""

import asyncio
import time
from typing import Optional, Dict, Any
from playwright.async_api import async_playwright, Browser, Page
import httpx
from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt, wait_exponential
from instagram_scraper.config import Config
from instagram_scraper.logger import setup_logger

logger = setup_logger()


class InstagramScraper:
    """Instagram profile scraper."""
    
    def __init__(self):
        self.config = Config()
        self.browser: Optional[Browser] = None
        self.context = None
        self.page: Optional[Page] = None
        self.cookies = None
        self.logged_in = False
        
    async def __aenter__(self):
        """Async context manager entry."""
        await self.start()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
        
    async def start(self):
        """Initialize browser and login."""
        playwright = await async_playwright().start()
        
        launch_options = {
            "headless": True,
            "args": ["--no-sandbox", "--disable-setuid-sandbox"]
        }
        
        if Config.PROXY_URL:
            proxy_parts = Config.PROXY_URL.replace("http://", "").split(":")
            if len(proxy_parts) >= 2:
                launch_options["proxy"] = {
                    "server": Config.PROXY_URL
                }
        
        self.browser = await playwright.chromium.launch(**launch_options)
        self.context = await self.browser.new_context(
            viewport={"width": 1280, "height": 720},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        self.page = await self.context.new_page()
        
        await self._login()
        
    async def _login(self):
        """Login to Instagram using Playwright."""
        logger.info("Starting Instagram login...")
        
        try:
            await self.page.goto("https://www.instagram.com/accounts/login/", timeout=30000)
            await asyncio.sleep(2)
            
            await self.page.fill('input[name="username"]', Config.INSTAGRAM_USERNAME)
            await self.page.fill('input[name="password"]', Config.INSTAGRAM_PASSWORD)
            
            await self.page.click('button[type="submit"]')
            await asyncio.sleep(5)
            
            current_url = self.page.url
            if "challenge" in current_url or "two_factor" in current_url:
                logger.warning("Two-factor authentication or challenge detected")
                self.logged_in = False
                return
            
            self.cookies = await self.context.cookies()
            self.logged_in = True
            logger.info("Successfully logged in to Instagram")
            
        except Exception as e:
            logger.error(f"Login failed: {str(e)}")
            self.logged_in = False
            
    async def close(self):
        """Close browser and cleanup."""
        if self.page:
            await self.page.close()
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
            
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=10))
    async def scrape_profile(self, username: str) -> Dict[str, Any]:
        """Scrape a single Instagram profile."""
        result = {
            "username": username,
            "display_name": "",
            "bio": "",
            "email": "",
            "phone": "",
            "links": "",
            "gender": "",
            "age": "",
            "region": "",
            "warning_code": "",
            "error": ""
        }
        
        try:
            logger.info(f"Scraping profile: {username}")
            
            url = f"https://www.instagram.com/{username}/"
            
            await self.page.goto(url, wait_until="networkidle", timeout=30000)
            await asyncio.sleep(Config.RATE_LIMIT_DELAY)
            
            content = await self.page.content()
            
            if not self.logged_in:
                result["warning_code"] = "NOT_LOGGED_IN"
                logger.warning(f"Not logged in when scraping {username}")
            
            result.update(self._parse_profile(content))
            
            logger.info(f"Successfully scraped profile: {username}")
            
        except Exception as e:
            error_msg = str(e)
            result["error"] = error_msg
            logger.error(f"Error scraping {username}: {error_msg}")
            
        return result
        
    def _parse_profile(self, html_content: str) -> Dict[str, Any]:
        """Parse profile data from HTML using BeautifulSoup."""
        soup = BeautifulSoup(html_content, 'lxml')
        data = {}
        
        try:
            meta_desc = soup.find('meta', {'property': 'og:description'})
            if meta_desc and meta_desc.get('content'):
                desc = meta_desc['content']
                data['display_name'] = desc.split(' ')[0] if desc else ""
            
            title = soup.find('title')
            if title:
                title_text = title.text
                if '(@' in title_text:
                    data['display_name'] = title_text.split('(@')[0].strip()
            
            scripts = soup.find_all('script', type='application/ld+json')
            for script in scripts:
                if script.string and '"@type":"Person"' in script.string:
                    import json
                    try:
                        json_data = json.loads(script.string)
                        if 'name' in json_data:
                            data['display_name'] = json_data['name']
                    except:
                        pass
            
            bio_elements = soup.find_all(['span', 'div'], class_=lambda x: x and 'bio' in x.lower())
            for elem in bio_elements:
                if elem.text.strip():
                    data['bio'] = elem.text.strip()
                    break
            
            link_elements = soup.find_all('a', href=True)
            external_links = []
            for link in link_elements:
                href = link['href']
                if href.startswith('http') and 'instagram.com' not in href:
                    external_links.append(href)
            
            if external_links:
                data['links'] = ';'.join(external_links[:3])
            
        except Exception as e:
            logger.error(f"Error parsing profile: {str(e)}")
            
        return data
        
    async def scrape_profiles(self, usernames: list[str]) -> list[Dict[str, Any]]:
        """Scrape multiple profiles with rate limiting."""
        results = []
        
        for username in usernames:
            result = await self.scrape_profile(username)
            results.append(result)
            
            await asyncio.sleep(Config.RATE_LIMIT_DELAY)
            
        return results
