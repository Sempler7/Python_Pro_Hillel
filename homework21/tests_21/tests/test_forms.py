import datetime
import pytest
from forms import TaskForm

# Функціональний стиль
def test_valid_form():
    form = TaskForm(data={
        "title": "Test Task",
        "description": "Some description",
        "due_date": datetime.date.today() + datetime.timedelta(days=1)
    })
    assert form.is_valid()

def test_empty_title():
    form = TaskForm(data={
        "title": "",
        "due_date": datetime.date.today() + datetime.timedelta(days=1)
    })
    assert not form.is_valid()
    assert "title" in form.errors

def test_due_date_in_past():
    form = TaskForm(data={
        "title": "Test Task",
        "due_date": datetime.date.today() - datetime.timedelta(days=1)
    })
    assert not form.is_valid()
    assert "due_date" in form.errors


# ООП стиль
class TestTaskForm:
    def test_valid_form(self):
        form = TaskForm(data={
            "title": "Task",
            "due_date": datetime.date.today() + datetime.timedelta(days=1)
        })
        assert form.is_valid()

    def test_missing_title(self):
        form = TaskForm(data={
            "title": "",
            "due_date": datetime.date.today() + datetime.timedelta(days=1)
        })
        assert not form.is_valid()

    def test_due_date_past(self):
        form = TaskForm(data={
            "title": "Task",
            "due_date": datetime.date.today() - datetime.timedelta(days=1)
        })
        assert not form.is_valid()
