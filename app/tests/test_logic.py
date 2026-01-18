import pytest
from app.src.models import User, Task

def test_user_to_dict():
    """Test User.to_dict() method"""
    user = User(
        id=1,
        username="testuser",
        email="test@example.com",
        created_at=datetime(2024, 1, 1)
    )
    
    result = user.to_dict()
    
    assert result['id'] == 1
    assert result['username'] == "testuser"
    assert result['email'] == "test@example.com"
    assert 'created_at' in result

def test_task_to_dict():
    """Test Task.to_dict() method"""
    task = Task(
        id=1,
        title="Test Task",
        description="Test Description",
        status="pending",
        user_id=1,
        created_at=datetime(2024, 1, 1),
        updated_at=datetime(2024, 1, 1)
    )
    
    result = task.to_dict()
    
    assert result['id'] == 1
    assert result['title'] == "Test Task"
    assert result['status'] == "pending"
    assert 'created_at' in result
    assert 'updated_at' in result