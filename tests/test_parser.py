"""Tests for parser module."""

import pytest
from igscraper.parser import InstagramParser


class TestInstagramParser:
    """Test cases for InstagramParser."""

    def setup_method(self):
        """Setup test fixtures."""
        self.parser = InstagramParser()

    def test_parse_user_profile_with_empty_html(self):
        """Test parsing user profile with empty HTML."""
        html = ""
        result = self.parser.parse_user_profile(html)
        
        assert isinstance(result, dict)
        assert 'username' in result
        assert 'full_name' in result
        assert 'bio' in result
        assert 'followers' in result
        assert result['followers'] == 0

    def test_parse_user_profile_with_meta_tags(self):
        """Test parsing user profile with meta tags."""
        html = """
        <html>
        <head>
            <meta property="og:title" content="Test User • Instagram" />
            <meta property="og:description" content="This is a test bio" />
            <meta property="og:image" content="https://example.com/image.jpg" />
        </head>
        </html>
        """
        result = self.parser.parse_user_profile(html)
        
        assert result['full_name'] == 'Test User'
        assert result['bio'] == 'This is a test bio'
        assert result['profile_pic_url'] == 'https://example.com/image.jpg'

    def test_parse_post_with_empty_html(self):
        """Test parsing post with empty HTML."""
        html = ""
        result = self.parser.parse_post(html)
        
        assert isinstance(result, dict)
        assert 'post_id' in result
        assert 'caption' in result
        assert 'likes' in result
        assert result['likes'] == 0

    def test_parse_post_with_image(self):
        """Test parsing post with image."""
        html = """
        <html>
        <head>
            <meta property="og:description" content="Test caption" />
            <meta property="og:image" content="https://example.com/post.jpg" />
        </head>
        </html>
        """
        result = self.parser.parse_post(html)
        
        assert result['caption'] == 'Test caption'
        assert result['image_url'] == 'https://example.com/post.jpg'
        assert result['is_video'] is False

    def test_parse_post_with_video(self):
        """Test parsing post with video."""
        html = """
        <html>
        <head>
            <meta property="og:description" content="Video caption" />
            <meta property="og:video" content="https://example.com/video.mp4" />
        </head>
        </html>
        """
        result = self.parser.parse_post(html)
        
        assert result['caption'] == 'Video caption'
        assert result['video_url'] == 'https://example.com/video.mp4'
        assert result['is_video'] is True

    def test_extract_usernames_from_page(self):
        """Test extracting usernames from page."""
        html = """
        <html>
        <body>
            <a href="/testuser1/">User 1</a>
            <a href="/testuser2/">User 2</a>
            <a href="/explore/">Explore</a>
            <a href="/p/abc123/">Post</a>
        </body>
        </html>
        """
        result = self.parser.extract_usernames_from_page(html)
        
        assert 'testuser1' in result
        assert 'testuser2' in result
        assert 'explore' not in result
        assert len(result) == 2

    def test_extract_hashtags(self):
        """Test extracting hashtags from text."""
        text = "This is a test #hashtag1 and #hashtag2 #hashtag1"
        result = self.parser.extract_hashtags(text)
        
        assert 'hashtag1' in result
        assert 'hashtag2' in result
        assert len(result) == 2  # Duplicates removed

    def test_extract_hashtags_empty_text(self):
        """Test extracting hashtags from empty text."""
        text = ""
        result = self.parser.extract_hashtags(text)
        
        assert result == []

    def test_extract_hashtags_no_hashtags(self):
        """Test extracting hashtags from text without hashtags."""
        text = "This text has no hashtags"
        result = self.parser.extract_hashtags(text)
        
        assert result == []
