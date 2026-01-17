from datetime import datetime, timedelta
import time
from typing import Optional
from jose import JWTError, jwt
from src.core.config import settings
from sqlmodel import Session
from src.models.task import Task
from fastapi import HTTPException, status
import bcrypt


def verify_token(token: str) -> Optional[dict]:
    """
    Verify JWT token from Better Auth using shared BETTER_AUTH_SECRET.
    """
    try:
        payload = jwt.decode(
            token, settings.BETTER_AUTH_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )

        # Check if token is expired using UTC timestamp
        exp = payload.get("exp")
        if exp and exp < time.time():
            return None

        return payload
    except JWTError:
        return None
    except Exception:
        return None


def get_current_user_id(token: str) -> Optional[str]:
    """
    Extract user ID from JWT token.
    """
    payload = verify_token(token)
    if payload:
        # Extract user ID from token - typically stored as 'sub' or 'user_id'
        user_id = payload.get("sub") or payload.get("user_id")
        return user_id
    return None


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create access token.
    """
    to_encode = data.copy()
    now = time.time()
    if expires_delta:
        expire = now + expires_delta.total_seconds()
    else:
        expire = now + (settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.BETTER_AUTH_SECRET, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def get_password_hash(password: str) -> str:
    # Hash a password for the first time
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
