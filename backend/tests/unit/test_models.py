import pytest
from datetime import datetime
from src.models.task import Task, TaskCreate


def test_task_creation():
    """Test creating a Task instance."""
    task_data = {
        "title": "Test Task",
        "description": "Test Description",
        "completed": False,
        "user_id": "user_123"
    }

    task = Task(**task_data)

    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.completed is False
    assert task.user_id == "user_123"
    assert task.id is None  # Should be None initially


def test_task_update_timestamp():
    """Test that the updated_at timestamp is updated when fields change."""
    task = Task(
        title="Original Task",
        description="Original Description",
        completed=False,
        user_id="user_123"
    )

    original_updated_at = task.updated_at

    # Simulate updating a field
    task.title = "Updated Task"

    # updated_at should have changed
    assert task.updated_at > original_updated_at


def test_task_create_model():
    """Test creating a TaskCreate instance."""
    task_create = TaskCreate(
        title="Test Task",
        description="Test Description",
        completed=False,
        user_id="user_123"
    )

    assert task_create.title == "Test Task"
    assert task_create.description == "Test Description"
    assert task_create.completed is False
    assert task_create.user_id == "user_123"


def test_task_validation_title_required():
    """Test that title is required."""
    # This should fail validation if title is empty
    with pytest.raises(ValueError):
        TaskCreate(
            title="",  # Empty title should fail
            description="Test Description",
            completed=False,
            user_id="user_123"
        )


def test_task_validation_title_length():
    """Test that title length is validated."""
    # This should fail if title is too long
    long_title = "x" * 256  # 256 characters, exceeding max length of 255
    with pytest.raises(ValueError):
        TaskCreate(
            title=long_title,
            description="Test Description",
            completed=False,
            user_id="user_123"
        )