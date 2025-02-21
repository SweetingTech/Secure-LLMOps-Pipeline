import pytest
from datetime import datetime, timedelta
from fastapi import Request, HTTPException
from app.middleware.rate_limiter import RateLimiter

class MockRequest:
    def __init__(self, client_host):
        self.client = type('MockClient', (), {'host': client_host})

@pytest.fixture
def rate_limiter():
    return RateLimiter(requests_per_minute=2)

@pytest.mark.asyncio
async def test_rate_limiter_basic(rate_limiter):
    request = MockRequest("127.0.0.1")
    
    # First request should pass
    assert await rate_limiter.check_rate_limit(request) is True
    
    # Second request should pass
    assert await rate_limiter.check_rate_limit(request) is True
    
    # Third request should fail (exceeds rate limit)
    with pytest.raises(HTTPException) as exc_info:
        await rate_limiter.check_rate_limit(request)
    assert exc_info.value.status_code == 429
    assert "rate limit exceeded" in str(exc_info.value.detail).lower()

@pytest.mark.asyncio
async def test_rate_limiter_multiple_clients(rate_limiter):
    client1 = MockRequest("127.0.0.1")
    client2 = MockRequest("127.0.0.2")
    
    # Client 1 requests
    assert await rate_limiter.check_rate_limit(client1) is True
    assert await rate_limiter.check_rate_limit(client1) is True
    
    # Client 2 should not be affected by Client 1's rate limit
    assert await rate_limiter.check_rate_limit(client2) is True
    assert await rate_limiter.check_rate_limit(client2) is True
    
    # Both clients should hit rate limit on next request
    with pytest.raises(HTTPException):
        await rate_limiter.check_rate_limit(client1)
    with pytest.raises(HTTPException):
        await rate_limiter.check_rate_limit(client2)

def test_clean_old_requests(rate_limiter):
    client_id = "127.0.0.1"
    now = datetime.now()
    
    # Add some old requests
    rate_limiter.requests[client_id] = [
        now - timedelta(minutes=2),  # Old request
        now - timedelta(seconds=30),  # Recent request
        now,  # Current request
    ]
    
    rate_limiter._clean_old_requests(client_id)
    
    # Should only have the recent requests (less than 1 minute old)
    assert len(rate_limiter.requests[client_id]) == 2

@pytest.mark.asyncio
async def test_rate_limiter_request_cleanup(rate_limiter):
    request = MockRequest("127.0.0.1")
    
    # Add some old requests that should be cleaned up
    now = datetime.now()
    rate_limiter.requests[request.client.host] = [
        now - timedelta(minutes=2),
        now - timedelta(minutes=1, seconds=30),
    ]
    
    # New request should pass because old requests were cleaned up
    assert await rate_limiter.check_rate_limit(request) is True
    assert await rate_limiter.check_rate_limit(request) is True
    
    # Third request should fail
    with pytest.raises(HTTPException):
        await rate_limiter.check_rate_limit(request)

@pytest.mark.asyncio
async def test_rate_limiter_reset(rate_limiter):
    request = MockRequest("127.0.0.1")
    
    # Use up the rate limit
    await rate_limiter.check_rate_limit(request)
    await rate_limiter.check_rate_limit(request)
    
    # Wait for the rate limit window to pass
    rate_limiter.requests[request.client.host] = [
        datetime.now() - timedelta(minutes=2)
    ]
    
    # Should be able to make requests again
    assert await rate_limiter.check_rate_limit(request) is True
