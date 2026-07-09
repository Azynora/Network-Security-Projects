# 📊 03 - Simple SIEM

## Description / Mô tả

**EN:** Collect Linux system logs via journalctl, store them in SQLite, and detect anomalous behavior.

**VI:** Thu thập log hệ thống Linux qua journalctl, lưu trữ vào SQLite, và phát hiện hành vi bất thường.

## Features / Tính năng
- [x] Collect logs via journalctl (JSON format, no regex needed) / Thu thập log qua journalctl (JSON format, không cần regex)
- [x] Normalize logs to a unified format / Chuẩn hóa log thành format thống nhất
- [x] Store in SQLite with deduplication logic (avoid duplicate storage) / Lưu vào SQLite với dedup logic (tránh lưu trùng)
- [x] Query logs by priority, unit / Truy vấn log theo priority, unit
- [x] Detect sudo brute-force (multiple failed password attempts) / Phát hiện sudo brute-force (nhiều lần nhập sai password)
- [x] Detect failed SSH login attempts / Phát hiện SSH login thất bại
- [x] Push logs to Elasticsearch (bulk indexing, deduplication via SQLite ID) / Đẩy log lên Elasticsearch (bulk indexing, dedup bằng SQLite id)
- [x] Grafana dashboard: Log Volume, Priority Distribution, Top Units, Recent Logs / Dashboard Grafana: Log Volume, Priority Distribution, Top Units, Recent Logs

## Skills / Kỹ năng
Python  Linux systemd/journald  SQLite  Log parsing

## Usage / Cách chạy

```bash
source venv/bin/activate

# Collect logs from the last 60 minutes and save to SQLite / Thu thập log 60 phút gần đây và lưu vào SQLite
venv/bin/python src/main.py collect --minutes 60 --save

# View only error/warning logs, do not save / Chỉ xem log lỗi/cảnh báo, không lưu
venv/bin/python src/main.py collect --minutes 30 --priority err

# Detect anomalous behavior from stored logs / Phát hiện hành vi bất thường từ log đã lưu
venv/bin/python src/main.py detect --sudo-threshold 3
```

## Structure / Cấu trúc
```
src/
├── main.py              # entry point, CLI sub-commands
└── siem/
    ├── journal_reader.py # read logs via journalctl
    ├── storage.py        # SQLite: init, save, query
    ├── detection.py      # brute-force detection, failed SSH detection
    └── display.py        # pretty-print results
```

## Technical Notes / Ghi chú kỹ thuật

**EN:**
- Garuda Linux (and other systemd-based distros) lacks the traditional /var/log/syslog. Logs are accessed via journalctl -o json, which already provides structured JSON, so no regex parsing is needed.
- Syslog priority levels: 0=EMERG, 1=ALERT, 2=CRIT, 3=ERR, 4=WARNING, 5=NOTICE, 6=INFO, 7=DEBUG.
- Deduplication logic is based on (timestamp, pid, message) to avoid storing duplicate logs when running collect multiple times.
- To read logs without sudo, the user must belong to the systemd-journal group: sudo usermod -aG systemd-journal \cauchunho then log out and back in.

**VI:**
- Garuda Linux (và các distro dùng systemd) không có /var/log/syslog truyền thống. Log được truy cập qua journalctl -o json, tự động có cấu trúc JSON sẵn, không cần viết regex.
- Priority theo chuẩn syslog: 0=EMERG, 1=ALERT, 2=CRIT, 3=ERR, 4=WARNING, 5=NOTICE, 6=INFO, 7=DEBUG.
- Dedup logic dựa trên (timestamp, pid, message) để tránh lưu trùng log khi chạy collect nhiều lần.
- Cần user thuộc group systemd-journal để đọc log không cần sudo: sudo usermod -aG systemd-journal \cauchunho rồi logout/login lại.

## Stack
Python  SQLite  Elasticsearch 8.13  Grafana 10.4  Docker Compose

## Usage with Elasticsearch and Grafana / Cách chạy (kèm Elasticsearch và Grafana)

```bash
# 1. Start Docker stack / Khởi động Docker stack
cd docker && docker compose up -d

# 2. Collect logs and save to SQLite / Thu thập log và lưu SQLite
venv/bin/python src/main.py collect --minutes 60 --save

# 3. Index to Elasticsearch / Đẩy lên Elasticsearch
venv/bin/python src/main.py index

# 4. Detect anomalies / Phát hiện bất thường
venv/bin/python src/main.py detect --sudo-threshold 3

# 5. View dashboard / Xem dashboard
# Open http://localhost:3000 (admin/admin)
```

## Screenshots
![Grafana Dashboard](docs/screenshots/Screenshot_20260709_211508.png)
