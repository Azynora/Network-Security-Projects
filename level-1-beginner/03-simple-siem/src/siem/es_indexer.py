"""Đẩy log từ SQLite lên Elasticsearch để Grafana có thể truy vấn"""

from elasticsearch import Elasticsearch, helpers
from datetime import datetime
from rich.console import Console
import sqlite3
import os

console = Console()

ES_HOST = "http://localhost:9200"
INDEX_NAME = "siem-logs"

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "db", "siem.db")

PRIORITY_MAP = {
    "0": "EMERG", "1": "ALERT", "2": "CRIT", "3": "ERR",
    "4": "WARNING", "5": "NOTICE", "6": "INFO", "7": "DEBUG"
}


def get_es_client():
    return Elasticsearch(ES_HOST)


def create_index_if_not_exists(es):
    """Tạo index với mapping phù hợp nếu chưa tồn tại"""
    if es.indices.exists(index=INDEX_NAME):
        return

    mapping = {
        "mappings": {
            "properties": {
                "timestamp": {"type": "date"},
                "host": {"type": "keyword"},
                "unit": {"type": "keyword"},
                "priority": {"type": "keyword"},
                "priority_label": {"type": "keyword"},
                "message": {"type": "text"},
                "pid": {"type": "keyword"},
            }
        }
    }

    es.indices.create(index=INDEX_NAME, body=mapping)
    console.print(f"[green]✅ Đã tạo index '{INDEX_NAME}'[/green]")


def convert_journal_timestamp(raw_ts):
    """
    journalctl __REALTIME_TIMESTAMP là microseconds từ epoch, dạng string
    Chuyển sang ISO format để Elasticsearch hiểu đúng kiểu date
    """
    try:
        ts_seconds = int(raw_ts) / 1_000_000
        return datetime.utcfromtimestamp(ts_seconds).isoformat()
    except (ValueError, TypeError):
        return datetime.utcnow().isoformat()


def fetch_all_logs_from_sqlite(db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM logs")
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows


def index_logs_to_es(db_path=DB_PATH):
    """Đọc toàn bộ log từ SQLite, đẩy lên Elasticsearch (bulk insert)"""
    es = get_es_client()
    create_index_if_not_exists(es)

    logs = fetch_all_logs_from_sqlite(db_path)

    if not logs:
        console.print("[yellow]Không có log nào trong SQLite để đẩy lên[/yellow]")
        return 0

    actions = []
    for log in logs:
        doc = {
            "timestamp": convert_journal_timestamp(log["timestamp"]),
            "host": log["host"],
            "unit": log["unit"],
            "priority": log["priority"],
            "priority_label": PRIORITY_MAP.get(log["priority"], "UNKNOWN"),
            "message": log["message"],
            "pid": log["pid"],
        }
        actions.append({
            "_index": INDEX_NAME,
            "_id": log["id"],  # dùng id SQLite làm _id, tránh trùng khi chạy lại
            "_source": doc
        })

    success, errors = helpers.bulk(es, actions, raise_on_error=False)
    console.print(f"[green]✅ Đã index {success} log lên Elasticsearch[/green]")

    if errors:
        console.print(f"[red]⚠️  {len(errors)} lỗi khi index[/red]")

    return success


if __name__ == "__main__":
    index_logs_to_es()
