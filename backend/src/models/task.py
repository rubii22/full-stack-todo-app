from sqlmodel import SQLModel, Field, Column
from typing import Optional
from datetime import datetime
import uuid


class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    user_id: str = Field(index=True)  # Foreign key to users table (managed by Better Auth)


class Task(TaskBase, table=True):
    """
    Task model representing a user's task with properties:
    - id: Auto-incrementing primary key
    - user_id: Foreign key to users.id from Better Auth
    - title: Task title (required, max 255 chars)
    - description: Task description (optional, max 1000 chars)
    - completed: Task completion status (default: False)
    - created_at: Task creation timestamp (auto-generated)
    - updated_at: Task last update timestamp (auto-generated)
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Update updated_at on modification
    def __setattr__(self, name, value):
        if name == "updated_at":
            # Allow explicit setting of updated_at
            super().__setattr__(name, value)
        elif name in ["title", "description", "completed"]:
            # Update updated_at when important fields change
            super().__setattr__("updated_at", datetime.utcnow())
            super().__setattr__(name, value)
        else:
            super().__setattr__(name, value)


class TaskUpdate(SQLModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: Optional[bool] = Field(default=None)


class TaskCreate(TaskBase):
    pass  # Inherits all fields from TaskBase