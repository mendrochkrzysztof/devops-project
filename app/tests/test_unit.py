import pytest
from app.src.models import User, Task
from datetime import datetime

def test_user_model():
    """Test User model creation"""
    user = User(
        username="testuser",
        email="test@example.com"
    )
    
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert isinstance(user.created_at, datetime)

def test_task_model():
    """Test Task model creation"""
    task = Task(
        title="Test Task",
        description="Test Description",
        user_id=1
    )
    
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.status == "pending"
    assert task.user_id == 1