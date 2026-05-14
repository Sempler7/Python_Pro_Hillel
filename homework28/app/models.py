from typing import Optional
from sqlmodel import SQLModel, Field


class Item(SQLModel, table=True):
    """Модель елемента в базі даних"""

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    price: float
    is_active: bool = True
    owner_id: int


class ItemCreate(SQLModel):
    """Схема для створення нового елемента"""

    title: str
    description: Optional[str] = None
    price: float
    owner_id: int


class ItemRead(SQLModel):
    """Схема для читання даних елемента"""

    id: int
    title: str
    description: Optional[str] = None
    price: float
    is_active: bool
    owner_id: int


class ItemUpdate(SQLModel):
    """Схема для оновлення існуючого елемента"""

    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    is_active: Optional[bool] = None