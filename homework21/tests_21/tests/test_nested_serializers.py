import datetime
import pytest
from serializers import TaskWithUserSerializer

def test_valid_nested_serializer():
    data = {
        "title": "Task",
        "description": "Desc",
        "due_date": datetime.date.today() + datetime.timedelta(days=1),
        "user": {"username": "testuser", "email": "test@example.com"}
    }
    serializer = TaskWithUserSerializer(data=data)
    assert serializer.is_valid()

def test_invalid_nested_serializer():
    data = {
        "title": "Task",
        "due_date": datetime.date.today() + datetime.timedelta(days=1),
        "user": {"username": "", "email": "invalid"}
    }
    serializer = TaskWithUserSerializer(data=data)
    assert not serializer.is_valid()
    assert "user" in serializer.errors
