"""Đọc log hệ thống Linux qua journalctl"""

import subprocess
import json

PRIORITY_MAP = {
    "0": "EMERG", "1": "ALERT", "2": "CRIT", "3": "ERR",
    "4": "WARNING", "5": "NOTICE", "6": "INFO", "7": "DEBUG"
}


def read_journal_logs(minutes=10, priority=None):
    cmd = ["journalctl", "-o", "json", f"--since=-{minutes}min"]

    if priority:
        cmd += ["-p", priority]

    result = subprocess.run(cmd, capture_output=True, text=True)

    logs = []
    for line in result.stdout.strip().split("\n"):
        if not line:
            continue
        try:
            entry = json.loads(line)
            logs.append(normalize_entry(entry))
        except json.JSONDecodeError:
            continue

    return logs


def normalize_entry(entry):
    return {
        "timestamp": entry.get("__REALTIME_TIMESTAMP", ""),
        "host": entry.get("_HOSTNAME", "N/A"),
        "unit": entry.get("_SYSTEMD_UNIT", entry.get("SYSLOG_IDENTIFIER", "N/A")),
        "priority": str(entry.get("PRIORITY", "6")),
        "message": entry.get("MESSAGE", ""),
        "pid": entry.get("_PID", "N/A"),
    }

