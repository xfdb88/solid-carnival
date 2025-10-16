"""Command-line interface for Instagram scraper."""

import asyncio
import sys
from pathlib import Path
import click

from .config import Config
from .scraper import InstagramScraper
from .log import setup_logger


@click.group()
@click.version_option(version="0.1.0")
def main():
    """Instagram Scraper CLI - A tool to scrape Instagram data."""
    pass


@main.command()
@click.option(
    '--input',
    '-i',
    'input_file',
    type=click.Path(exists=True, path_type=Path),
    default=Path('data/input.csv'),
    help='Input CSV file containing usernames'
)
@click.option(
    '--output',
    '-o',
    'output_file',
    type=click.Path(path_type=Path),
    default=Path('data/output.csv'),
    help='Output CSV file for results'
)
@click.option(
    '--env-file',
    '-e',
    type=click.Path(exists=True),
    default='.env',
    help='Environment file path'
)
@click.option(
    '--headless/--no-headless',
    default=True,
    help='Run browser in headless mode'
)
def scrape(input_file: Path, output_file: Path, env_file: str, headless: bool):
    """Scrape Instagram user profiles from input file."""
    
    # Load configuration
    config = Config(env_file=env_file)
    
    # Setup logger
    logger = setup_logger(level=config.log_level)
    
    try:
        logger.info("Starting Instagram scraper...")
        logger.info(f"Input file: {input_file}")
        logger.info(f"Output file: {output_file}")
        
        # Load input usernames
        usernames = InstagramScraper.load_input(input_file)
        logger.info(f"Loaded {len(usernames)} usernames from input file")
        
        # Run scraper
        asyncio.run(_run_scraper(config, usernames, output_file, headless))
        
        logger.info("Scraping completed successfully")
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        sys.exit(1)


async def _run_scraper(
    config: Config,
    usernames: list,
    output_file: Path,
    headless: bool
):
    """Run the scraper asynchronously."""
    async with InstagramScraper(config, headless=headless) as scraper:
        results = await scraper.scrape_users(usernames)
        scraper.save_results(results, output_file)


@main.command()
@click.argument('username')
@click.option(
    '--env-file',
    '-e',
    type=click.Path(exists=True),
    default='.env',
    help='Environment file path'
)
@click.option(
    '--headless/--no-headless',
    default=True,
    help='Run browser in headless mode'
)
def profile(username: str, env_file: str, headless: bool):
    """Scrape a single Instagram user profile."""
    
    # Load configuration
    config = Config(env_file=env_file)
    
    # Setup logger
    logger = setup_logger(level=config.log_level)
    
    try:
        logger.info(f"Scraping profile: {username}")
        
        # Run scraper
        result = asyncio.run(_scrape_profile(config, username, headless))
        
        # Display results
        click.echo("\nProfile Information:")
        click.echo("-" * 50)
        for key, value in result.items():
            if key != 'error':
                click.echo(f"{key}: {value}")
        
        if 'error' in result:
            click.echo(f"\nError: {result['error']}", err=True)
            sys.exit(1)
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        sys.exit(1)


async def _scrape_profile(config: Config, username: str, headless: bool):
    """Scrape a single profile asynchronously."""
    async with InstagramScraper(config, headless=headless) as scraper:
        return await scraper.scrape_user_profile(username)


@main.command()
def init():
    """Initialize project structure and create example files."""
    
    click.echo("Initializing Instagram scraper project...")
    
    # Create directories
    dirs = [Path('data'), Path('logs')]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
        click.echo(f"Created directory: {d}")
    
    # Create .env file if it doesn't exist
    env_file = Path('.env')
    if not env_file.exists():
        env_content = """# Instagram Scraper Configuration

# Instagram credentials
IG_USERNAME=your_username
IG_PASSWORD=your_password

# Rate limiting settings
RATE_LIMIT_REQUESTS=10
RATE_LIMIT_PERIOD=60

# Output settings
OUTPUT_DIR=data
LOG_LEVEL=INFO
"""
        env_file.write_text(env_content)
        click.echo(f"Created .env file: {env_file}")
    else:
        click.echo(f".env file already exists: {env_file}")
    
    # Create example input.csv
    input_file = Path('data/input.csv')
    if not input_file.exists():
        input_content = "username\nexample_user1\nexample_user2\n"
        input_file.write_text(input_content)
        click.echo(f"Created example input file: {input_file}")
    else:
        click.echo(f"Input file already exists: {input_file}")
    
    click.echo("\nInitialization complete!")
    click.echo("Please update your .env file with your Instagram credentials.")


if __name__ == '__main__':
    main()
