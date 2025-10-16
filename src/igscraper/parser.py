"""HTML parser for Instagram content."""

from typing import Dict, List, Optional, Any
from bs4 import BeautifulSoup


class InstagramParser:
    """Parser for Instagram HTML content."""

    @staticmethod
    def parse_user_profile(html: str) -> Dict[str, Any]:
        """Parse user profile information from HTML.
        
        Args:
            html: HTML content of user profile page
            
        Returns:
            Dictionary containing user profile information
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        profile_data = {
            'username': '',
            'full_name': '',
            'bio': '',
            'followers': 0,
            'following': 0,
            'posts': 0,
            'profile_pic_url': '',
            'is_verified': False,
            'is_private': False,
        }
        
        # Try to extract data from meta tags
        og_title = soup.find('meta', property='og:title')
        if og_title:
            content = og_title.get('content', '')
            if content:
                parts = content.split('•')
                if parts:
                    profile_data['full_name'] = parts[0].strip()
        
        og_description = soup.find('meta', property='og:description')
        if og_description:
            profile_data['bio'] = og_description.get('content', '')
        
        og_image = soup.find('meta', property='og:image')
        if og_image:
            profile_data['profile_pic_url'] = og_image.get('content', '')
        
        return profile_data

    @staticmethod
    def parse_post(html: str) -> Dict[str, Any]:
        """Parse post information from HTML.
        
        Args:
            html: HTML content of post page
            
        Returns:
            Dictionary containing post information
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        post_data = {
            'post_id': '',
            'username': '',
            'caption': '',
            'likes': 0,
            'comments': 0,
            'timestamp': '',
            'image_url': '',
            'video_url': '',
            'is_video': False,
        }
        
        # Try to extract data from meta tags
        og_description = soup.find('meta', property='og:description')
        if og_description:
            post_data['caption'] = og_description.get('content', '')
        
        og_image = soup.find('meta', property='og:image')
        if og_image:
            post_data['image_url'] = og_image.get('content', '')
        
        og_video = soup.find('meta', property='og:video')
        if og_video:
            post_data['video_url'] = og_video.get('content', '')
            post_data['is_video'] = True
        
        return post_data

    @staticmethod
    def extract_usernames_from_page(html: str) -> List[str]:
        """Extract usernames from a page.
        
        Args:
            html: HTML content
            
        Returns:
            List of usernames found on the page
        """
        soup = BeautifulSoup(html, 'html.parser')
        usernames = []
        
        # Look for links to user profiles
        links = soup.find_all('a', href=True)
        for link in links:
            href = link['href']
            if href.startswith('/') and not any(
                x in href for x in ['explore', 'p/', 'reel/', 'tv/', 'direct']
            ):
                username = href.strip('/').split('/')[0]
                if username and username not in usernames:
                    usernames.append(username)
        
        return usernames

    @staticmethod
    def extract_hashtags(text: str) -> List[str]:
        """Extract hashtags from text.
        
        Args:
            text: Text to extract hashtags from
            
        Returns:
            List of hashtags (without # symbol)
        """
        import re
        hashtags = re.findall(r'#(\w+)', text)
        return list(set(hashtags))
