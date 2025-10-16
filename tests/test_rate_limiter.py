"""Tests for RateLimiter"""

import pytest
import time
from igscraper.rate_limiter import RateLimiter


class TestRateLimiter:
    """Test cases for RateLimiter"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.rate_limiter = RateLimiter(max_requests=5, time_window=10)
    
    def test_rate_limiter_initialization(self):
        """Test rate limiter initialization"""
        assert self.rate_limiter is not None
        assert self.rate_limiter.max_requests == 5
        assert self.rate_limiter.time_window == 10
        assert len(self.rate_limiter.requests) == 0
    
    def test_can_proceed_initially(self):
        """Test that requests can proceed initially"""
        assert self.rate_limiter.can_proceed() is True
    
    def test_record_request(self):
        """Test recording a request"""
        initial_count = len(self.rate_limiter.requests)
        self.rate_limiter.record_request()
        
        assert len(self.rate_limiter.requests) == initial_count + 1
    
    def test_multiple_requests(self):
        """Test multiple requests within limit"""
        for i in range(4):
            result = self.rate_limiter.request()
            assert result is True
        
        assert len(self.rate_limiter.requests) == 4
    
    def test_rate_limit_reached(self):
        """Test behavior when rate limit is reached"""
        # Fill up to the limit
        for i in range(5):
            self.rate_limiter.record_request()
        
        # Should not be able to proceed
        assert self.rate_limiter.can_proceed() is False
    
    def test_clean_old_requests(self):
        """Test cleaning of old requests"""
        # Record a request
        self.rate_limiter.record_request()
        
        # Manually set an old timestamp
        self.rate_limiter.requests[0] = time.time() - 11
        
        # Clean old requests
        self.rate_limiter._clean_old_requests()
        
        # Old request should be removed
        assert len(self.rate_limiter.requests) == 0
    
    def test_reset(self):
        """Test reset functionality"""
        # Add some requests
        for i in range(3):
            self.rate_limiter.record_request()
        
        assert len(self.rate_limiter.requests) == 3
        
        # Reset
        self.rate_limiter.reset()
        
        assert len(self.rate_limiter.requests) == 0
    
    def test_get_stats(self):
        """Test getting rate limiter stats"""
        self.rate_limiter.record_request()
        self.rate_limiter.record_request()
        
        stats = self.rate_limiter.get_stats()
        
        assert stats is not None
        assert stats['current_requests'] == 2
        assert stats['max_requests'] == 5
        assert stats['time_window'] == 10
        assert stats['requests_available'] == 3
    
    def test_wait_if_needed_no_wait(self):
        """Test wait_if_needed when no wait is required"""
        result = self.rate_limiter.wait_if_needed()
        assert result is None
    
    def test_requests_available_after_time_window(self):
        """Test that requests become available after time window"""
        limiter = RateLimiter(max_requests=2, time_window=1)
        
        # Fill the limit
        limiter.record_request()
        limiter.record_request()
        
        # Should not be able to proceed
        assert limiter.can_proceed() is False
        
        # Wait for time window to pass
        time.sleep(1.1)
        
        # Should be able to proceed now
        assert limiter.can_proceed() is True
