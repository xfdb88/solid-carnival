"""Instagram Scraper Package

A Python package for scraping Instagram data using Playwright.
"""

__version__ = "0.1.0"
__author__ = "solid-carnival"

from .scraper import InstagramScraper
from .config import Config

__all__ = ["InstagramScraper", "Config"]
