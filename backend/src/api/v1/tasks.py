from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import asc, desc
from src.database.session import get_async_session
from src.schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskListResponse
from src.models.task import Task, TaskCreate as TaskCreateModel
from src.api.deps import get_current_user
from datetime import datetime


router = APIRouter()


@router.get("/", response_model=TaskListResponse)
async def get_tasks(
    current_user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
    status_filter: Optional[str] = Query(None, description="Filter by status: all, pending, completed"),
    sort: Optional[str] = Query("created_at", description="Sort by field: created_at, title, updated_at"),
    order: Optional[str] = Query("asc", description="Sort order: asc, desc"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Number of items per page")
):
    """
    Get all tasks for the authenticated user with optional filtering and sorting.
    """
    # Build query with user isolation
    query = select(Task).where(Task.user_id == current_user_id)

    # Apply status filter
    if status_filter and status_filter != "all":
        if status_filter == "pending":
            query = query.where(Task.completed == False)
        elif status_filter == "completed":
            query = query.where(Task.completed == True)

    # Apply sorting
    if sort == "created_at":
        sort_field = Task.created_at
    elif sort == "title":
        sort_field = Task.title
    elif sort == "updated_at":
        sort_field = Task.updated_at
    else:
        sort_field = Task.created_at

    if order == "desc":
        query = query.order_by(desc(sort_field))
    else:
        query = query.order_by(asc(sort_field))

    # Apply pagination
    offset = (page - 1) * limit
    query = query.offset(offset).limit(limit)

    # Execute query
    result = await db.execute(query)
    tasks = result.scalars().all()

    # Get total count for pagination metadata
    count_query = select(Task).where(Task.user_id == current_user_id)
    if status_filter and status_filter != "all":
        if status_filter == "pending":
            count_query = count_query.where(Task.completed == False)
        elif status_filter == "completed":
            count_query = count_query.where(Task.completed == True)
    count_result = await db.execute(count_query)
    total = len(count_result.scalars().all())

    return TaskListResponse(
        tasks=tasks,
        total=total,
        page=page,
        limit=limit
    )


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_create: TaskCreate,
    current_user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
    """
    Create a new task for the authenticated user.
    """
    # Create task with user_id from authenticated user
    task = Task(
        title=task_create.title,
        description=task_create.description,
        completed=task_create.completed,
        user_id=current_user_id
    )

    db.add(task)
    await db.commit()
    await db.refresh(task)

    return task


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    current_user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
    """
    Get a specific task by ID for the authenticated user.
    """
    # Query task with user isolation
    result = await db.execute(
        select(Task).where(Task.id == task_id).where(Task.user_id == current_user_id)
    )
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    current_user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
    """
    Update a specific task by ID for the authenticated user.
    """
    # Query task with user isolation
    result = await db.execute(
        select(Task).where(Task.id == task_id).where(Task.user_id == current_user_id)
    )
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Update fields that are provided
    if task_update.title is not None:
        task.title = task_update.title
    if task_update.description is not None:
        task.description = task_update.description
    if task_update.completed is not None:
        task.completed = task_update.completed

    # Update the updated_at timestamp
    task.updated_at = datetime.utcnow()

    await db.commit()
    await db.refresh(task)

    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    current_user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
    """
    Delete a specific task by ID for the authenticated user.
    """
    # Query task with user isolation
    result = await db.execute(
        select(Task).where(Task.id == task_id).where(Task.user_id == current_user_id)
    )
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    await db.delete(task)
    await db.commit()

    return