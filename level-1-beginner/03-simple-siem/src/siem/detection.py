"""Phát hiện hành vi bất thường từ log đã lưu"""

import sqlite3
from collections import defaultdict
from siem.storage import DB_PATH


def detect_sudo_brute_force(threshold=3, db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM logs
        WHERE message LIKE '%password is required%'
           OR message LIKE '%authentication failure%'
           OR message LIKE '%Invalid password%'
        ORDER BY timestamp ASC
    """)

    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()

    user_counter = defaultdict(list)
    for row in rows:
        message = row["message"]
        user = message.split(":")[0].strip() if ":" in message else "unknown"
        user_counter[user].append(row)

    return {user: entries for user, entries in user_counter.items() if len(entries) >= threshold}


def detect_failed_ssh_login(threshold=3, db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM logs
        WHERE (unit LIKE '%sshd%' OR message LIKE '%sshd%')
          AND (message LIKE '%Failed password%' OR message LIKE '%Failed publickey%')
        ORDER BY timestamp ASC
    """)

    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return rows
