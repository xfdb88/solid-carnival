"""Command-line interface for Instagram Scraper"""

import asyncio
import argparse
import sys
from pathlib import Path

from .config import Config
from .scraper import InstagramScraper
from .log import setup_logging, get_logger


def main():
    """Main entry point for CLI"""
    parser = argparse.ArgumentParser(
        description="Instagram Scraper - Scrape Instagram profiles using Playwright"
    )
    
    parser.add_argument(
        '-i', '--input',
        type=str,
        help='Input CSV file containing usernames to scrape'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        help='Output CSV file for scraped data'
    )
    
    parser.add_argument(
        '-u', '--username',
        type=str,
        help='Instagram username for login'
    )
    
    parser.add_argument(
        '-p', '--password',
        type=str,
        help='Instagram password for login'
    )
    
    parser.add_argument(
        '--env',
        type=str,
        help='Path to .env file'
    )
    
    parser.add_argument(
        '--headless',
        action='store_true',
        help='Run browser in headless mode'
    )
    
    parser.add_argument(
        '--log-level',
        type=str,
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        default='INFO',
        help='Logging level'
    )
    
    parser.add_argument(
        '--log-file',
        type=str,
        help='Path to log file'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(
        log_level=args.log_level,
        log_file=args.log_file
    )
    
    logger = get_logger(__name__)
    logger.info("Instagram Scraper started")
    
    try:
        # Load configuration
        config = Config(env_file=args.env)
        
        # Override config with command-line arguments
        if args.username:
            config.username = args.username
        if args.password:
            config.password = args.password
        if args.input:
            config.input_file = args.input
        if args.output:
            config.output_file = args.output
        if args.headless:
            config.headless = True
        
        # Validate configuration
        if not config.validate():
            logger.error("Invalid configuration. Please provide username and password.")
            sys.exit(1)
        
        # Check if input file exists
        input_path = Path(config.input_file)
        if not input_path.exists():
            logger.error(f"Input file not found: {config.input_file}")
            sys.exit(1)
        
        # Run scraper
        asyncio.run(run_scraper(config))
        
    except KeyboardInterrupt:
        logger.info("Scraper interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Scraper error: {str(e)}", exc_info=True)
        sys.exit(1)


async def run_scraper(config: Config):
    """Run the scraper with given configuration
    
    Args:
        config: Configuration object
    """
    logger = get_logger(__name__)
    scraper = InstagramScraper(config)
    
    try:
        # Scrape profiles
        results = await scraper.scrape_profiles_from_file()
        
        if results:
            # Save results
            scraper.save_to_csv()
            logger.info(f"Scraping completed. {len(results)} profiles scraped.")
        else:
            logger.warning("No profiles were scraped")
        
    finally:
        # Cleanup
        await scraper.close()


if __name__ == "__main__":
    main()
