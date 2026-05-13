from ninja import Schema
from datetime import datetime


class ServerIn(Schema):
    """Схема для створення або оновлення сервера"""

    name: str
    ip_address: str
    status: str = "online"


class ServerOut(Schema):
    """Схема відповіді для сервера"""

    id: int
    name: str
    ip_address: str
    status: str
    created_at: datetime


class ServerStatusIn(Schema):
    """Схема для оновлення статусу сервера"""

    status: str


class MetricIn(Schema):
    """Схема для створення метрик сервера"""

    cpu: float
    memory: float
    load: float


class MetricOut(Schema):
    """Схема відповіді для метрик сервера"""

    id: int
    server_id: int
    cpu: float
    memory: float
    load: float
    recorded_at: datetime


class AlertOut(Schema):
    """Схема відповіді для сповіщення"""

    id: int
    server_id: int
    message: str
    created_at: datetime