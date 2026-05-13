from ninja import Schema
from typing import List
from datetime import datetime


class TagIn(Schema):
    """Схема для створення тегу"""

    name: str


class TagOut(Schema):
    """Схема для відображення тегу"""

    id: int
    name: str


class CommentIn(Schema):
    """Схема для створення коментаря"""

    text: str


class CommentOut(Schema):
    """Схема для відображення коментаря"""

    id: int
    author_id: int
    text: str
    created_at: datetime


class PostIn(Schema):
    """Схема для створення або оновлення посту"""

    title: str
    content: str
    tag_ids: List[int] = []


class PostOut(Schema):
    """Схема для відображення посту з тегами та коментарями"""

    id: int
    title: str
    content: str
    author_id: int
    tags: List[TagOut]
    comments: List[CommentOut]
    created_at: datetime
    updated_at: datetime