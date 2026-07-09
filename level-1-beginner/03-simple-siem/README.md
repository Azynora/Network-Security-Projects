# 📊 03 - Simple SIEM

## Mô tả
Thu thập log hệ thống Linux qua journalctl, lưu trữ vào SQLite, và phát hiện hành vi bất thường.

## Tính năng
- [x] Thu thập log qua `journalctl` (JSON format, không cần regex)
- [x] Chuẩn hóa log thành format thống nhất
- [x] Lưu vào SQLite với dedup logic (tránh lưu trùng)
- [x] Truy vấn log theo priority, unit
- [x] Phát hiện sudo brute-force (nhiều lần nhập sai password)
- [x] Phát hiện SSH login thất bại
- [x] Đẩy log lên Elasticsearch (bulk indexing, dedup bằng SQLite id)
- [x] Dashboard Grafana: Log Volume, Priority Distribution, Top Units, Recent Logs

## Kỹ năng
`Python` `Linux systemd/journald` `SQLite` `Log parsing`

## Cách chạy

```bash
source venv/bin/activate

# Thu thập log 60 phút gần đây và lưu vào SQLite
venv/bin/python src/main.py collect --minutes 60 --save

# Chỉ xem log lỗi/cảnh báo, không lưu
venv/bin/python src/main.py collect --minutes 30 --priority err

# Phát hiện hành vi bất thường từ log đã lưu
venv/bin/python src/main.py detect --sudo-threshold 3
```

## Cấu trúc
src/
├── main.py              # entry point, CLI sub-commands
└── siem/
├── journal_reader.py # đọc log qua journalctl
├── storage.py         # SQLite: init, save, query
├── detection.py       # brute-force, failed SSH detection
└── display.py          # in bảng kết quả

## Ghi chú kỹ thuật
- Garuda Linux (và các distro dùng systemd) không có `/var/log/syslog` truyền thống.
  Log được truy cập qua `journalctl -o json`, tự động có cấu trúc JSON sẵn, không cần viết regex.
- Priority theo chuẩn syslog: 0=EMERG, 1=ALERT, 2=CRIT, 3=ERR, 4=WARNING, 5=NOTICE, 6=INFO, 7=DEBUG.
- Dedup logic dựa trên (timestamp, pid, message) để tránh lưu trùng log khi chạy collect nhiều lần.
- Cần user thuộc group `systemd-journal` để đọc log không cần sudo:
  `sudo usermod -aG systemd-journal $USER` rồi logout/login lại.

## Stack
`Python` `SQLite` `Elasticsearch 8.13` `Grafana 10.4` `Docker Compose`

## Cách chạy

```bash
# 1. Khởi động Docker stack
cd docker && docker compose up -d

# 2. Thu thập log và lưu SQLite
venv/bin/python src/main.py collect --minutes 60 --save

# 3. Đẩy lên Elasticsearch
venv/bin/python src/main.py index

# 4. Phát hiện bất thường
venv/bin/python src/main.py detect --sudo-threshold 3

# 5. Xem dashboard
# Mở http://localhost:3000 (admin/admin)
```

## Screenshots
![Grafana Dashboard](docs/screenshots/grafana-dashboard.png)
![Detection Output](docs/screenshots/detection-output.png)
