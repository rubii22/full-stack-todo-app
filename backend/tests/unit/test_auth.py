import pytest
from datetime import datetime, timedelta
from jose import jwt
from src.auth.utils import verify_token, get_current_user_id
from src.core.config import settings


def test_verify_valid_token():
    """Test that a valid JWT token can be verified."""
    # Create a valid token
    data = {"sub": "test_user_123", "exp": (datetime.utcnow() + timedelta(minutes=30)).timestamp()}
    token = jwt.encode(data, settings.BETTER_AUTH_SECRET, algorithm=settings.JWT_ALGORITHM)

    # Verify the token
    payload = verify_token(token)
    assert payload is not None
    assert payload["sub"] == "test_user_123"


def test_verify_expired_token():
    """Test that an expired JWT token is rejected."""
    # Create an expired token
    data = {"sub": "test_user_123", "exp": (datetime.utcnow() - timedelta(minutes=30)).timestamp()}
    token = jwt.encode(data, settings.BETTER_AUTH_SECRET, algorithm=settings.JWT_ALGORITHM)

    # Verify the token (should return None for expired)
    payload = verify_token(token)
    assert payload is None


def test_verify_invalid_signature():
    """Test that a token with invalid signature is rejected."""
    # Create a token with different secret
    wrong_secret = "wrong_secret_different_from_actual"
    data = {"sub": "test_user_123", "exp": (datetime.utcnow() + timedelta(minutes=30)).timestamp()}
    token = jwt.encode(data, wrong_secret, algorithm=settings.JWT_ALGORITHM)

    # Verify the token (should return None for invalid signature)
    payload = verify_token(token)
    assert payload is None


def test_get_current_user_id_valid():
    """Test that a valid token returns the correct user ID."""
    # Create a valid token
    data = {"sub": "test_user_123", "exp": (datetime.utcnow() + timedelta(minutes=30)).timestamp()}
    token = jwt.encode(data, settings.BETTER_AUTH_SECRET, algorithm=settings.JWT_ALGORITHM)

    # Get user ID
    user_id = get_current_user_id(token)
    assert user_id == "test_user_123"


def test_get_current_user_id_invalid():
    """Test that an invalid token returns None."""
    # Use an invalid token
    invalid_token = "invalid.token.string"
    user_id = get_current_user_id(invalid_token)
    assert user_id is None