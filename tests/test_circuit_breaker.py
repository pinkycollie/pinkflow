"""
Tests for circuit breaker functionality.
"""
import pytest
from app.core.circuit_breaker import CircuitBreaker, CircuitBreakerOpenError


def test_circuit_breaker_closed_state():
    """Test circuit breaker in closed state allows calls."""
    cb = CircuitBreaker(failure_threshold=3, recovery_timeout=1)
    
    @cb
    def successful_function():
        return "success"
    
    result = successful_function()
    assert result == "success"
    assert cb.state == 'CLOSED'


def test_circuit_breaker_opens_after_failures():
    """Test circuit breaker opens after threshold failures."""
    cb = CircuitBreaker(failure_threshold=3, recovery_timeout=1)
    
    @cb
    def failing_function():
        raise Exception("Service unavailable")
    
    # First 3 failures should be raised
    for i in range(3):
        with pytest.raises(Exception, match="Service unavailable"):
            failing_function()
    
    # Circuit should now be open
    assert cb.state == 'OPEN'
    
    # Next call should fail fast with CircuitBreakerOpenError
    with pytest.raises(CircuitBreakerOpenError):
        failing_function()


def test_circuit_breaker_half_open_recovery():
    """Test circuit breaker transitions to half-open and recovers."""
    import time
    
    cb = CircuitBreaker(failure_threshold=2, recovery_timeout=1)
    
    call_count = [0]
    
    @cb
    def sometimes_failing_function():
        call_count[0] += 1
        if call_count[0] <= 2:
            raise Exception("Initial failures")
        return "success"
    
    # Cause failures to open circuit
    for i in range(2):
        with pytest.raises(Exception):
            sometimes_failing_function()
    
    assert cb.state == 'OPEN'
    
    # Wait for recovery timeout
    time.sleep(1.1)
    
    # Next call should succeed and close circuit
    result = sometimes_failing_function()
    assert result == "success"
    assert cb.state == 'CLOSED'


def test_circuit_breaker_reset():
    """Test manual reset of circuit breaker."""
    cb = CircuitBreaker(failure_threshold=2, recovery_timeout=60)
    
    @cb
    def failing_function():
        raise Exception("Error")
    
    # Open the circuit
    for i in range(2):
        with pytest.raises(Exception):
            failing_function()
    
    assert cb.state == 'OPEN'
    
    # Reset the circuit
    cb.reset()
    
    assert cb.state == 'CLOSED'
    assert cb.failure_count == 0


def test_circuit_breaker_get_state():
    """Test getting circuit breaker state."""
    cb = CircuitBreaker(failure_threshold=3)
    
    state = cb.get_state()
    assert state['state'] == 'CLOSED'
    assert state['failure_count'] == 0
    assert state['last_failure_time'] is None
