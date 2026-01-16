from fastapi import Request, HTTPException, status
from fastapi.security.http import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response
from src.auth.utils import verify_token


class AuthMiddleware(BaseHTTPMiddleware):
    """
    Global authentication middleware for all /api/ routes.

    This middleware automatically validates JWT tokens for all API routes
    and attaches user information to the request state.
    """

    def __init__(self, app, exempt_paths: Optional[list] = None):
        super().__init__(app)
        self.exempt_paths = exempt_paths or [
            "/health",
            "/docs",
            "/redoc",
            "/openapi.json",
            "/api/auth/login",
            "/api/auth/signup",
        ]
        self.security = HTTPBearer(
            auto_error=False
        )  # Don't auto-error, handle manually

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        # Skip authentication for exempt paths
        if request.url.path in self.exempt_paths or request.url.path.startswith(
            "/api/docs"
        ):
            response = await call_next(request)
            return response

        # Skip authentication for non-API routes (for now, we'll protect all /api/ routes)
        if (
            not request.url.path.startswith("/api/")
            or request.url.path == "/api/health"
        ):
            response = await call_next(request)
            return response

        # Extract authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization header missing",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Verify token
        token = auth_header.replace("Bearer ", "")
        payload = verify_token(token)

        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Add user info to request state for use in endpoints
        user_id = payload.get("sub") or payload.get("user_id")
        if user_id:
            request.state.user_id = user_id
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User ID not found in token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        response = await call_next(request)
        return response


# Alternative: A simpler approach using dependency injection at the router level
# This is often preferred in FastAPI applications
from fastapi import Depends
from src.api.deps import get_current_user


def get_auth_dependency():
    """
    Returns the authentication dependency for use in routes.
    This can be used to add authentication to specific routes or routers.
    """
    return Depends(get_current_user)
