import pytest
from httpx import AsyncClient
from src.main import app
from src.database.config import engine, AsyncSessionLocal
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import StaticPool


@pytest.mark.asyncio
async def test_health_endpoint():
    """Test that the health endpoint works."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


@pytest.mark.asyncio
async def test_api_routes_exist():
    """Test that API routes exist (will return 401 due to auth but should exist)."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Test that we get a 401 (unauthorized) rather than 404 (not found)
        # This indicates the route exists but requires authentication
        response = await ac.get("/api/tasks")

    # Should return 401 due to missing authentication, not 404
    # Note: FastAPI's default behavior might return 422 for missing auth header
    assert response.status_code in [401, 422]  # Could be either depending on auth setup


@pytest.mark.asyncio
async def test_create_task_missing_auth():
    """Test that creating a task without auth returns 401."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/tasks", json={
            "title": "Test task",
            "description": "Test description"
        })

    # Should return 401 due to missing authentication
    assert response.status_code in [401, 422]  # Could be either depending on auth setup