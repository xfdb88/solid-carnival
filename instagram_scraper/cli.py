"""Command-line interface for Instagram scraper."""

import argparse
import asyncio
import csv
import sys
from pathlib import Path
from instagram_scraper.config import Config
from instagram_scraper.scraper import InstagramScraper
from instagram_scraper.logger import setup_logger

logger = setup_logger()


def read_usernames(input_file: Path) -> list[str]:
    """Read usernames from CSV file."""
    usernames = []
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if 'username' in row and row['username'].strip():
                    usernames.append(row['username'].strip())
        
        logger.info(f"Read {len(usernames)} usernames from {input_file}")
        return usernames
        
    except FileNotFoundError:
        logger.error(f"Input file not found: {input_file}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error reading input file: {str(e)}")
        sys.exit(1)


def write_results(output_file: Path, results: list[dict]):
    """Write results to CSV file."""
    if not results:
        logger.warning("No results to write")
        return
    
    fieldnames = [
        "username", "display_name", "bio", "email", "phone", 
        "links", "gender", "age", "region", "warning_code", "error"
    ]
    
    try:
        with open(output_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
        
        logger.info(f"Results written to {output_file}")
        
    except Exception as e:
        logger.error(f"Error writing output file: {str(e)}")
        sys.exit(1)


async def run_scraper(input_file: Path, output_file: Path):
    """Run the scraper."""
    try:
        Config.validate()
    except ValueError as e:
        logger.error(str(e))
        sys.exit(1)
    
    usernames = read_usernames(input_file)
    
    if not usernames:
        logger.error("No usernames found in input file")
        sys.exit(1)
    
    logger.info(f"Starting scraper for {len(usernames)} profiles")
    
    async with InstagramScraper() as scraper:
        results = await scraper.scrape_profiles(usernames)
    
    write_results(output_file, results)
    logger.info("Scraping completed")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Instagram Profile Scraper - Scrape public Instagram profiles",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m instagram_scraper.cli
  python -m instagram_scraper.cli -i data/custom_input.csv -o data/custom_output.csv

Note: Make sure to configure your Instagram credentials in .env file before running.
        """
    )
    
    parser.add_argument(
        '-i', '--input',
        type=Path,
        default=Config.INPUT_CSV,
        help=f'Input CSV file with usernames (default: {Config.INPUT_CSV})'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=Path,
        default=Config.OUTPUT_CSV,
        help=f'Output CSV file for results (default: {Config.OUTPUT_CSV})'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='Instagram Scraper 1.0.0'
    )
    
    args = parser.parse_args()
    
    try:
        asyncio.run(run_scraper(args.input, args.output))
    except KeyboardInterrupt:
        logger.info("Scraper interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
