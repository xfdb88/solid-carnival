"""Rate limiter for controlling request frequency"""

import time
from collections import deque
from typing import Optional
from .log import get_logger

logger = get_logger(__name__)


class RateLimiter:
    """Rate limiter using token bucket algorithm"""
    
    def __init__(self, max_requests: int = 10, time_window: int = 60):
        """Initialize rate limiter
        
        Args:
            max_requests: Maximum number of requests allowed in time window
            time_window: Time window in seconds
        """
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests: deque = deque()
        
        logger.info(
            f"Rate limiter initialized: {max_requests} requests per {time_window}s"
        )
    
    def _clean_old_requests(self):
        """Remove requests older than the time window"""
        current_time = time.time()
        while self.requests and current_time - self.requests[0] > self.time_window:
            self.requests.popleft()
    
    def can_proceed(self) -> bool:
        """Check if a new request can proceed
        
        Returns:
            True if request can proceed, False otherwise
        """
        self._clean_old_requests()
        return len(self.requests) < self.max_requests
    
    def wait_if_needed(self) -> Optional[float]:
        """Wait if rate limit is exceeded
        
        Returns:
            Time waited in seconds, or None if no wait was needed
        """
        self._clean_old_requests()
        
        if len(self.requests) >= self.max_requests:
            # Calculate wait time
            oldest_request = self.requests[0]
            wait_time = self.time_window - (time.time() - oldest_request)
            
            if wait_time > 0:
                logger.warning(
                    f"Rate limit reached. Waiting {wait_time:.2f} seconds..."
                )
                time.sleep(wait_time)
                self._clean_old_requests()
                return wait_time
        
        return None
    
    def record_request(self):
        """Record a new request"""
        self._clean_old_requests()
        self.requests.append(time.time())
        logger.debug(
            f"Request recorded. Current count: {len(self.requests)}/{self.max_requests}"
        )
    
    def request(self) -> bool:
        """Execute a rate-limited request
        
        Returns:
            True if request was allowed, False otherwise
        """
        self.wait_if_needed()
        
        if self.can_proceed():
            self.record_request()
            return True
        
        return False
    
    def reset(self):
        """Reset the rate limiter"""
        self.requests.clear()
        logger.info("Rate limiter reset")
    
    def get_stats(self) -> dict:
        """Get current rate limiter statistics
        
        Returns:
            Dictionary with current stats
        """
        self._clean_old_requests()
        return {
            'current_requests': len(self.requests),
            'max_requests': self.max_requests,
            'time_window': self.time_window,
            'requests_available': self.max_requests - len(self.requests)
        }
