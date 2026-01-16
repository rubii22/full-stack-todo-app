from sqlmodel import create_engine, SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.core.config import settings
import asyncio


# Ensure DATABASE_URL uses asyncpg for async engine
db_url = settings.DATABASE_URL
if db_url.startswith("postgresql://"):
    db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)

# Robust strip of sslmode and other libpq-specific params
if "?" in db_url:
    base, query = db_url.split("?", 1)
    params = query.split("&")
    # Filter out libpq-specific params like sslmode, channel_binding
    new_params = [
        p
        for p in params
        if not p.startswith("sslmode=") and not p.startswith("channel_binding=")
    ]
    if new_params:
        db_url = f"{base}?{'&'.join(new_params)}"
    else:
        db_url = base

# Create async engine
engine = create_async_engine(
    db_url,
    echo=True if settings.DEBUG else False,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    pool_recycle=300,
)


# Create session maker for async sessions
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
)


async def create_db_and_tables():
    """Create database tables"""
    # Import all models here to ensure they are registered with SQLModel.metadata
    from src.models.task import Task
    from src.models.user import User

    async with engine.begin() as conn:
        # Create all tables defined in SQLModel models
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_async_session():
    """Get async session for dependency injection"""
    async with AsyncSessionLocal() as session:
        yield session
