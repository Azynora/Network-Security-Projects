"""Lưu và truy vấn log qua SQLite"""

import sqlite3
import os
from rich.console import Console

console = Console()

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "db", "siem.db")


def init_db(db_path=DB_PATH):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            host TEXT,
            unit TEXT,
            priority TEXT,
            message TEXT,
            pid TEXT,
            inserted_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_priority ON logs(priority)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_unit ON logs(unit)")

    conn.commit()
    conn.close()


def save_logs(logs, db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    inserted = 0
    for log in logs:
        cursor.execute("""
            SELECT COUNT(*) FROM logs
            WHERE timestamp = ? AND pid = ? AND message = ?
        """, (log["timestamp"], str(log["pid"]), log["message"]))

        exists = cursor.fetchone()[0] > 0

        if not exists:
            cursor.execute("""
                INSERT INTO logs (timestamp, host, unit, priority, message, pid)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (log["timestamp"], log["host"], log["unit"], log["priority"], log["message"], str(log["pid"])))
            inserted += 1

    conn.commit()
    conn.close()

    console.print(f"[green]✅ Đã lưu {inserted} log mới vào database (bỏ qua {len(logs) - inserted} trùng)[/green]")
    return inserted


def query_logs(priority=None, unit=None, limit=50, db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = "SELECT * FROM logs WHERE 1=1"
    params = []

    if priority:
        query += " AND priority = ?"
        params.append(priority)

    if unit:
        query += " AND unit LIKE ?"
        params.append(f"%{unit}%")

    query += " ORDER BY id DESC LIMIT ?"
    params.append(limit)

    cursor.execute(query, params)
    rows = [dict(row) for row in cursor.fetchall()]

    conn.close()
    return rows


def count_by_priority(db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT priority, COUNT(*) FROM logs GROUP BY priority ORDER BY COUNT(*) DESC")
    result = cursor.fetchall()

    conn.close()
    return result
