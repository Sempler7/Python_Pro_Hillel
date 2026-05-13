import datetime
import pytest
from serializers import TaskSerializer

def test_valid_serializer():
    data = {
        "title": "Task",
        "description": "Desc",
        "due_date": datetime.date.today() + datetime.timedelta(days=1)
    }
    serializer = TaskSerializer(data=data)
    assert serializer.is_valid()

def test_missing_title():
    data = {
        "description": "Desc",
        "due_date": datetime.date.today() + datetime.timedelta(days=1)
    }
    serializer = TaskSerializer(data=data)
    assert not serializer.is_valid()
    assert "title" in serializer.errors

def test_due_date_in_past():
    data = {
        "title": "Task",
        "due_date": datetime.date.today() - datetime.timedelta(days=1)
    }
    serializer = TaskSerializer(data=data)
    assert not serializer.is_valid()
    assert "due_date" in serializer.errors
