from cassandra.cluster import Cluster  # type: ignore[import-untyped]
from uuid import uuid4
from datetime import datetime, timedelta

cluster = Cluster(['127.0.0.1'])
session = cluster.connect()

# Створення keyspace та таблиці
session.execute("""
CREATE KEYSPACE IF NOT EXISTS shop_logs
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}
""")

session.execute("USE shop_logs")

session.execute("""
                CREATE TABLE IF NOT EXISTS event_logs
                (
                    event_id
                    UUID
                    PRIMARY
                    KEY,
                    user_id
                    TEXT,
                    event_type
                    TEXT,
                    timestamp
                    TIMESTAMP,
                    metadata
                    TEXT
                )
                """)

# CREATE
session.execute("""
                INSERT INTO event_logs (event_id, user_id, event_type, timestamp, metadata)
                VALUES (%s, %s, %s, %s, %s)
                """, (uuid4(), "123", "login", datetime.now(), "IP=192.168.0.1"))

# READ (події за останні 24 години)
yesterday = datetime.now() - timedelta(days=1)
rows = session.execute("""
                       SELECT *
                       FROM event_logs
                       WHERE event_type = 'login'
                         AND timestamp
                           > %s
                       """, (yesterday,))
for row in rows:
    print(row)

# UPDATE
session.execute("""
                UPDATE event_logs
                SET metadata=%s
                WHERE event_id = %s
                """, ("IP=192.168.0.2", uuid4()))

# DELETE (старіші за 7 днів)
week_ago = datetime.now() - timedelta(days=7)
session.execute("""
                DELETE
                FROM event_logs
                WHERE timestamp < %s
                """, (week_ago,))
