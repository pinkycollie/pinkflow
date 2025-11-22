"""
Circuit Breaker implementation for resilience and graceful degradation.
Prevents cascading failures by monitoring and breaking problematic connections.
"""
from functools import wraps
import time
from threading import Lock


class CircuitBreaker:
    """
    Circuit breaker pattern implementation.
    
    States:
    - CLOSED: Normal operation, requests pass through
    - OPEN: Failure threshold reached, requests fail fast
    - HALF_OPEN: Testing if service recovered
    """
    
    def __init__(self, failure_threshold=5, recovery_timeout=60):
        """
        Initialize circuit breaker.
        
        Args:
            failure_threshold: Number of failures before opening circuit
            recovery_timeout: Seconds to wait before trying again
        """
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = 'CLOSED'  # CLOSED, OPEN, HALF_OPEN
        self._lock = Lock()
    
    def __call__(self, func):
        """
        Decorator to wrap a function with circuit breaker logic.
        
        Args:
            func: Function to wrap
            
        Returns:
            Wrapped function with circuit breaker
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            with self._lock:
                if self.state == 'OPEN':
                    if time.time() - self.last_failure_time > self.recovery_timeout:
                        self.state = 'HALF_OPEN'
                    else:
                        raise CircuitBreakerOpenError(
                            f"Circuit breaker is OPEN. Service unavailable."
                        )
            
            try:
                result = func(*args, **kwargs)
                
                with self._lock:
                    if self.state == 'HALF_OPEN':
                        self.state = 'CLOSED'
                        self.failure_count = 0
                
                return result
                
            except Exception as e:
                with self._lock:
                    self.failure_count += 1
                    self.last_failure_time = time.time()
                    
                    if self.failure_count >= self.failure_threshold:
                        self.state = 'OPEN'
                
                raise e
        
        return wrapper
    
    def reset(self):
        """Reset the circuit breaker to closed state."""
        with self._lock:
            self.failure_count = 0
            self.last_failure_time = None
            self.state = 'CLOSED'
    
    def get_state(self):
        """Get current state of the circuit breaker."""
        return {
            'state': self.state,
            'failure_count': self.failure_count,
            'last_failure_time': self.last_failure_time
        }


class CircuitBreakerOpenError(Exception):
    """Exception raised when circuit breaker is open."""
    pass
