from fastapi import FastAPI
from src.core.config import settings
from src.core.rate_limiter import add_rate_limiting
from src.core.logging_config import setup_logging
from fastapi.middleware.cors import CORSMiddleware


# Set up logging
setup_logging()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # For development, allow all. In production, specify frontend URL.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add rate limiting
add_rate_limiting(app)


@app.on_event("startup")
async def on_startup():
    from src.database.config import create_db_and_tables

    await create_db_and_tables()


# Import and include API routers (deferred to avoid circular imports)
try:
    from src.api.v1.router import api_router

    app.include_router(api_router, prefix=settings.API_V1_STR)
except Exception as e:
    print(f"Warning: Could not load API routes: {e}")


@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": "2026-01-15T10:00:00Z"}


@app.get("/")
async def root():
    return {"message": "Todo Backend API is running!", "status": "success"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
