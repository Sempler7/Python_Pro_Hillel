"""Приклад використання Redis для зберігання сесій користувачів."""

from datetime import datetime
import redis  # type: ignore[import-untyped]

r = redis.Redis(host='localhost', port=6379, db=0)

# CREATE (нова сесія)
SESSION_ID = "session:123"
r.hset(SESSION_ID, mapping={
    "user_id": "123",
    "session_token": "abc123",
    "login_time": datetime.now().isoformat()
})

# READ (отримати сесію)
print(r.hgetall(SESSION_ID))

# UPDATE (оновити час активності)
r.hset(SESSION_ID, "last_activity", datetime.now().isoformat())

# DELETE (видалити сесію)
r.delete(SESSION_ID)

# TTL (30 хвилин)
r.expire(SESSION_ID, 1800)
