"""Tests for rate limiter module."""

import pytest
import time
from igscraper.rate_limiter import RateLimiter


class TestRateLimiter:
    """Test cases for RateLimiter."""

    def test_initialization(self):
        """Test rate limiter initialization."""
        limiter = RateLimiter(max_requests=10, time_period=60)
        
        assert limiter.max_requests == 10
        assert limiter.time_period == 60
        assert len(limiter.requests) == 0

    def test_acquire_single_request(self):
        """Test acquiring permission for a single request."""
        limiter = RateLimiter(max_requests=5, time_period=1)
        
        result = limiter.acquire(timeout=1.0)
        
        assert result is True
        assert len(limiter.requests) == 1

    def test_acquire_multiple_requests(self):
        """Test acquiring permission for multiple requests."""
        limiter = RateLimiter(max_requests=5, time_period=1)
        
        for _ in range(5):
            result = limiter.acquire(timeout=1.0)
            assert result is True
        
        assert len(limiter.requests) == 5

    def test_acquire_exceeds_limit(self):
        """Test acquiring permission when limit is exceeded."""
        limiter = RateLimiter(max_requests=2, time_period=10)
        
        # First two requests should succeed
        assert limiter.acquire(timeout=0.1) is True
        assert limiter.acquire(timeout=0.1) is True
        
        # Third request should timeout
        assert limiter.acquire(timeout=0.1) is False

    def test_acquire_with_time_window(self):
        """Test acquiring permission with time window expiration."""
        limiter = RateLimiter(max_requests=2, time_period=1)
        
        # Use up the limit
        assert limiter.acquire(timeout=0.1) is True
        assert limiter.acquire(timeout=0.1) is True
        
        # Wait for window to expire
        time.sleep(1.1)
        
        # Should be able to make requests again
        assert limiter.acquire(timeout=0.1) is True

    def test_reset(self):
        """Test resetting the rate limiter."""
        limiter = RateLimiter(max_requests=5, time_period=1)
        
        # Make some requests
        limiter.acquire(timeout=1.0)
        limiter.acquire(timeout=1.0)
        assert len(limiter.requests) == 2
        
        # Reset
        limiter.reset()
        
        assert len(limiter.requests) == 0

    def test_get_remaining_requests(self):
        """Test getting remaining requests."""
        limiter = RateLimiter(max_requests=5, time_period=1)
        
        assert limiter.get_remaining_requests() == 5
        
        limiter.acquire(timeout=1.0)
        assert limiter.get_remaining_requests() == 4
        
        limiter.acquire(timeout=1.0)
        assert limiter.get_remaining_requests() == 3

    def test_get_remaining_requests_after_expiry(self):
        """Test getting remaining requests after time window expiry."""
        limiter = RateLimiter(max_requests=3, time_period=1)
        
        # Use up all requests
        limiter.acquire(timeout=1.0)
        limiter.acquire(timeout=1.0)
        limiter.acquire(timeout=1.0)
        assert limiter.get_remaining_requests() == 0
        
        # Wait for window to expire
        time.sleep(1.1)
        
        # Should have all requests available again
        assert limiter.get_remaining_requests() == 3

    def test_get_wait_time_no_wait(self):
        """Test getting wait time when no wait is needed."""
        limiter = RateLimiter(max_requests=5, time_period=1)
        
        assert limiter.get_wait_time() == 0.0

    def test_get_wait_time_with_wait(self):
        """Test getting wait time when wait is needed."""
        limiter = RateLimiter(max_requests=2, time_period=2)
        
        # Use up the limit
        limiter.acquire(timeout=1.0)
        limiter.acquire(timeout=1.0)
        
        # Should need to wait
        wait_time = limiter.get_wait_time()
        assert wait_time > 0
        assert wait_time <= 2

    def test_thread_safety(self):
        """Test thread safety of rate limiter."""
        import threading
        
        limiter = RateLimiter(max_requests=10, time_period=5)
        results = []
        
        def make_request():
            result = limiter.acquire(timeout=0.5)
            results.append(result)
        
        # Create multiple threads
        threads = [threading.Thread(target=make_request) for _ in range(15)]
        
        # Start all threads
        for thread in threads:
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Should have exactly 10 successful requests (within timeout)
        assert sum(results) == 10
        assert len([r for r in results if not r]) == 5
