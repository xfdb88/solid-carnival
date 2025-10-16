"""HTML parser for Instagram data"""

from typing import Dict, List, Optional
from bs4 import BeautifulSoup
from .log import get_logger

logger = get_logger(__name__)


class InstagramParser:
    """Parse Instagram HTML content"""
    
    def __init__(self):
        """Initialize parser"""
        self.soup: Optional[BeautifulSoup] = None
    
    def parse_html(self, html: str) -> BeautifulSoup:
        """Parse HTML content
        
        Args:
            html: Raw HTML string
            
        Returns:
            BeautifulSoup object
        """
        self.soup = BeautifulSoup(html, 'lxml')
        return self.soup
    
    def extract_profile_info(self, html: str) -> Dict[str, any]:
        """Extract profile information from Instagram profile page
        
        Args:
            html: HTML content of profile page
            
        Returns:
            Dictionary containing profile information
        """
        soup = self.parse_html(html)
        profile_info = {
            'username': '',
            'full_name': '',
            'bio': '',
            'followers': 0,
            'following': 0,
            'posts': 0,
            'is_verified': False,
            'is_private': False
        }
        
        try:
            # Extract username from meta tags
            username_meta = soup.find('meta', property='og:title')
            if username_meta:
                profile_info['username'] = username_meta.get('content', '').split('(')[0].strip()
            
            # Extract bio from meta tags
            bio_meta = soup.find('meta', property='og:description')
            if bio_meta:
                profile_info['bio'] = bio_meta.get('content', '')
            
            logger.info(f"Successfully parsed profile for {profile_info['username']}")
            
        except Exception as e:
            logger.error(f"Error parsing profile info: {str(e)}")
        
        return profile_info
    
    def extract_post_data(self, html: str) -> List[Dict[str, any]]:
        """Extract post data from Instagram page
        
        Args:
            html: HTML content containing posts
            
        Returns:
            List of dictionaries containing post information
        """
        soup = self.parse_html(html)
        posts = []
        
        try:
            # Extract post elements
            post_elements = soup.find_all('article') or []
            
            for post in post_elements:
                post_data = {
                    'caption': '',
                    'likes': 0,
                    'comments': 0,
                    'timestamp': '',
                    'url': ''
                }
                posts.append(post_data)
            
            logger.info(f"Successfully parsed {len(posts)} posts")
            
        except Exception as e:
            logger.error(f"Error parsing post data: {str(e)}")
        
        return posts
    
    def extract_hashtags(self, text: str) -> List[str]:
        """Extract hashtags from text
        
        Args:
            text: Text containing hashtags
            
        Returns:
            List of hashtags
        """
        import re
        hashtags = re.findall(r'#\w+', text)
        return [tag.lower() for tag in hashtags]
    
    def extract_mentions(self, text: str) -> List[str]:
        """Extract @mentions from text
        
        Args:
            text: Text containing mentions
            
        Returns:
            List of mentioned usernames
        """
        import re
        mentions = re.findall(r'@\w+', text)
        return [mention[1:] for mention in mentions]
