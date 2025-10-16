"""Tests for InstagramParser"""

import pytest
from igscraper.parser import InstagramParser


class TestInstagramParser:
    """Test cases for InstagramParser"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.parser = InstagramParser()
    
    def test_parser_initialization(self):
        """Test parser initialization"""
        assert self.parser is not None
        assert self.parser.soup is None
    
    def test_parse_html(self):
        """Test HTML parsing"""
        html = "<html><body><h1>Test</h1></body></html>"
        soup = self.parser.parse_html(html)
        
        assert soup is not None
        assert soup.find('h1').text == 'Test'
    
    def test_extract_hashtags(self):
        """Test hashtag extraction"""
        text = "This is a #test post with #multiple #hashtags"
        hashtags = self.parser.extract_hashtags(text)
        
        assert len(hashtags) == 3
        assert '#test' in hashtags
        assert '#multiple' in hashtags
        assert '#hashtags' in hashtags
    
    def test_extract_hashtags_empty(self):
        """Test hashtag extraction with no hashtags"""
        text = "This is a post without hashtags"
        hashtags = self.parser.extract_hashtags(text)
        
        assert len(hashtags) == 0
    
    def test_extract_mentions(self):
        """Test mention extraction"""
        text = "Hello @user1 and @user2!"
        mentions = self.parser.extract_mentions(text)
        
        assert len(mentions) == 2
        assert 'user1' in mentions
        assert 'user2' in mentions
    
    def test_extract_mentions_empty(self):
        """Test mention extraction with no mentions"""
        text = "This is a post without mentions"
        mentions = self.parser.extract_mentions(text)
        
        assert len(mentions) == 0
    
    def test_extract_profile_info(self):
        """Test profile info extraction"""
        html = """
        <html>
            <head>
                <meta property="og:title" content="username (@username)">
                <meta property="og:description" content="This is a bio">
            </head>
            <body></body>
        </html>
        """
        
        profile_info = self.parser.extract_profile_info(html)
        
        assert profile_info is not None
        assert 'username' in profile_info
        assert 'bio' in profile_info
        assert profile_info['bio'] == 'This is a bio'
    
    def test_extract_post_data(self):
        """Test post data extraction"""
        html = """
        <html>
            <body>
                <article>Post 1</article>
                <article>Post 2</article>
            </body>
        </html>
        """
        
        posts = self.parser.extract_post_data(html)
        
        assert posts is not None
        assert isinstance(posts, list)
