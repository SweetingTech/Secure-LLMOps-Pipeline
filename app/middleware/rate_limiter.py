from fastapi import Request, HTTPException
from datetime import datetime, timedelta
from typing import Dict, Tuple
import time

class RateLimiter:
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, list] = {}
        
    def _clean_old_requests(self, client_id: str):
        """Remove requests older than 1 minute"""
        now = datetime.now()
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if now - req_time < timedelta(minutes=1)
        ]

    async def check_rate_limit(self, request: Request):
        client_id = request.client.host
        now = datetime.now()

        if client_id not in self.requests:
            self.requests[client_id] = []
        
        self._clean_old_requests(client_id)
        
        if len(self.requests[client_id]) >= self.requests_per_minute:
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded. Please try again later."
            )
        
        self.requests[client_id].append(now)
        return True

rate_limiter = RateLimiter()
