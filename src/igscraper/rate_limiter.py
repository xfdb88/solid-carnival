"""Rate limiter for API requests."""

import time
from collections import deque
from threading import Lock
from typing import Optional


class RateLimiter:
    """Rate limiter using sliding window algorithm."""

    def __init__(self, max_requests: int = 10, time_period: int = 60):
        """Initialize rate limiter.
        
        Args:
            max_requests: Maximum number of requests allowed
            time_period: Time period in seconds
        """
        self.max_requests = max_requests
        self.time_period = time_period
        self.requests = deque()
        self.lock = Lock()

    def acquire(self, timeout: Optional[float] = None) -> bool:
        """Acquire permission to make a request.
        
        Args:
            timeout: Maximum time to wait for permission in seconds.
                    If None, wait indefinitely.
        
        Returns:
            True if permission granted, False if timeout occurred.
        """
        start_time = time.time()
        
        while True:
            with self.lock:
                current_time = time.time()
                
                # Remove requests outside the time window
                while self.requests and current_time - self.requests[0] > self.time_period:
                    self.requests.popleft()
                
                # Check if we can make a request
                if len(self.requests) < self.max_requests:
                    self.requests.append(current_time)
                    return True
            
            # Check timeout
            if timeout is not None and (time.time() - start_time) >= timeout:
                return False
            
            # Sleep briefly before retrying
            time.sleep(0.1)

    def reset(self):
        """Reset the rate limiter."""
        with self.lock:
            self.requests.clear()

    def get_remaining_requests(self) -> int:
        """Get number of remaining requests available.
        
        Returns:
            Number of requests that can be made without waiting.
        """
        with self.lock:
            current_time = time.time()
            
            # Remove requests outside the time window
            while self.requests and current_time - self.requests[0] > self.time_period:
                self.requests.popleft()
            
            return max(0, self.max_requests - len(self.requests))

    def get_wait_time(self) -> float:
        """Get time to wait before next request is available.
        
        Returns:
            Time in seconds to wait, or 0 if request can be made immediately.
        """
        with self.lock:
            current_time = time.time()
            
            # Remove requests outside the time window
            while self.requests and current_time - self.requests[0] > self.time_period:
                self.requests.popleft()
            
            if len(self.requests) < self.max_requests:
                return 0.0
            
            # Calculate wait time until oldest request expires
            return self.time_period - (current_time - self.requests[0])
