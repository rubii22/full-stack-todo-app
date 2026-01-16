from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from src.auth.utils import get_current_user_id
from src.database.session import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession


security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_async_session)
) -> str:
    """
    Get current authenticated user ID from JWT token.

    Args:
        credentials: HTTP Authorization credentials containing JWT token
        db: Database session (included for potential future user lookup)

    Returns:
        User ID if authentication successful

    Raises:
        HTTPException: If authentication fails (401 Unauthorized)
    """
    token = credentials.credentials

    user_id = get_current_user_id(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user_id


async def get_optional_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Optional[str]:
    """
    Get current authenticated user ID from JWT token (optional).

    Args:
        credentials: HTTP Authorization credentials containing JWT token

    Returns:
        User ID if authentication successful, None if invalid
    """
    token = credentials.credentials
    return get_current_user_id(token)