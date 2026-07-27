"""
core/rate_limiter.py — In-memory sliding-window rate limiter
"""

import time
from collections import defaultdict
from fastapi import Request, HTTPException

RATE_LIMIT_WINDOW       = 60   # seconds
RATE_LIMIT_MAX_REQUESTS = 30   # requests per window

_request_history: dict[str, list[float]] = defaultdict(list)


def check_rate_limit(request: Request) -> None:
    """
    Dependency that enforces a per-IP sliding-window rate limit.
    Raises HTTP 429 when the limit is exceeded.
    """
    ip  = request.client.host if request.client else "unknown"
    now = time.time()

    history = [t for t in _request_history[ip] if now - t < RATE_LIMIT_WINDOW]
    if len(history) >= RATE_LIMIT_MAX_REQUESTS:
        raise HTTPException(
            status_code=429,
            detail={
                "error": "rate_limit_exceeded",
                "message": "Too many requests. Please wait a moment and try again.",
                "retry_after": RATE_LIMIT_WINDOW,
            },
        )
    history.append(now)
    _request_history[ip] = history
