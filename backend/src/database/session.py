from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator


# Import the get_async_session function from config
from .config import get_async_session as get_db_session


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Get async database session for dependency injection.

    This function is a wrapper around the get_async_session from config
    to maintain consistency with the import pattern.
    """
    async for session in get_db_session():
        yield session