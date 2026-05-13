from typing import Optional, Any
from datetime import datetime, date

from ninja import Schema


class StudentIn(Schema):
    """Схема для створення або оновлення студента"""

    username: str
    phone: str = ""
    birth_date: Optional[date] = None


class StudentOut(Schema):
    """Схема відповіді для студента"""

    id: int
    user_id: int
    first_name: str
    last_name: str
    phone: str
    birth_date: Optional[date]
    created_at: datetime

    @staticmethod
    def resolve_first_name(obj: Any) -> str:
        """Отримує ім'я користувача зі зв'язаного об'єкта"""
        return obj.user.first_name

    @staticmethod
    def resolve_last_name(obj: Any) -> str:
        """Отримує прізвище користувача зі зв'язаного об'єкта"""
        return obj.user.last_name


class CourseIn(Schema):
    """Схема для створення або оновлення курсу"""

    title: str
    description: str = ""


class CourseOut(Schema):
    """Схема відповіді для курсу"""

    id: int
    title: str
    description: str
    average_grade: Optional[float]
    created_at: datetime


class EnrollmentOut(Schema):
    """Схема відповіді для запису на курс"""

    id: int
    student_id: int
    course_id: int
    grade: Optional[float]
    enrolled_at: datetime


class GradeIn(Schema):
    """Схема для встановлення оцінки"""

    grade: float