from fastapi import APIRouter
from src.api.v1 import tasks


api_router = APIRouter()
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])