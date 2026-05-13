from ninja import Schema
from datetime import date, datetime
from typing import Optional


class TaskIn(Schema):
    """Схема для створення або оновлення завдання"""

    title: str
    description: str = ""
    status: str = "pending"
    due_date: Optional[date] = None


class TaskOut(Schema):
    """Схема відповіді для завдання"""

    id: int
    title: str
    description: str
    status: str
    due_date: Optional[date]
    created_at: datetime
    owner_id: int