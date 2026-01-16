from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from src.core.config import settings
from sqlmodel import Session
from src.models.task import Task
from fastapi import HTTPException, status


def verify_token(token: str) -> Optional[dict]:
    """
    Verify JWT token from Better Auth using shared BETTER_AUTH_SECRET.

    Args:
        token: JWT token to verify

    Returns:
        Decoded token payload if valid, None if invalid
    """
    try:
        payload = jwt.decode(
            token,
            settings.BETTER_AUTH_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )

        # Check if token is expired
        exp = payload.get("exp")
        if exp and datetime.fromtimestamp(exp) < datetime.utcnow():
            return None

        return payload
    except JWTError:
        return None
    except Exception:
        return None


def get_current_user_id(token: str) -> Optional[str]:
    """
    Extract user ID from JWT token.

    Args:
        token: JWT token from Authorization header

    Returns:
        User ID if token is valid, None if invalid
    """
    payload = verify_token(token)
    if payload:
        # Extract user ID from token - typically stored as 'sub' or 'user_id'
        user_id = payload.get("sub") or payload.get("user_id")
        return user_id
    return None


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create access token (primarily for testing purposes since we're using Better Auth).

    Args:
        data: Data to encode in token
        expires_delta: Expiration time delta

    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire.timestamp()})
    encoded_jwt = jwt.encode(to_encode, settings.BETTER_AUTH_SECRET, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt