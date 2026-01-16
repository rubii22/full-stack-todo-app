from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from fastapi import FastAPI
from src.core.config import settings


# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)


def add_rate_limiting(app: FastAPI):
    """
    Add rate limiting to the FastAPI application.

    Args:
        app: FastAPI application instance
    """
    # Add rate limiter to app state
    app.state.limiter = limiter

    # Add rate limit exceeded handler
    app.add_exception_handler(429, _rate_limit_exceeded_handler)

    # Add middleware for rate limiting
    from slowapi.middleware import SlowAPIMiddleware
    app.add_middleware(SlowAPIMiddleware)


def get_rate_limit_config():
    """
    Get rate limit configuration based on environment.

    Returns:
        Dictionary with rate limit settings
    """
    if settings.ENVIRONMENT == "development":
        return {
            "requests_per_minute": 100,  # Higher rate limit for development
            "requests_per_hour": 1000
        }
    else:
        return {
            "requests_per_minute": 10,   # Conservative rate limit for production
            "requests_per_hour": 100
        }