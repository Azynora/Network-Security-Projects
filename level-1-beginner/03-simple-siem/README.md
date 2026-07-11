<a id="language"></a>

<div align="right">

## 🌐 Language

🇺🇸 [English](#english) | 🇻🇳 [Tiếng Việt](#tieng-viet)

</div>

---

<a id="english"></a>

# 🇺🇸 English

# 📊 03 - Simple SIEM

## Description

Collect Linux system logs via `journalctl`, store them in SQLite, detect anomalous behavior (brute-force attacks), and visualize data with Elasticsearch and Grafana dashboards.

## Features

- [x] Collect logs via journalctl (JSON format — no regex parsing needed)
- [x] Normalize logs to a unified format
- [x] Store in SQLite with deduplication (avoid storing duplicates)
- [x] Query logs by priority and unit
- [x] Detect sudo brute-force attacks (multiple failed password attempts)
- [x] Detect failed SSH login attempts
- [x] Push logs to Elasticsearch (bulk indexing with deduplication via SQLite ID)
- [x] Push alerts to a dedicated Elasticsearch index for alerting dashboards
- [x] Grafana dashboard: Log Volume, Priority Distribution, Top Units, Recent Logs

## Skills Practiced

`Python` `Linux systemd/journald` `SQLite` `Elasticsearch` `Grafana` `Docker Compose` `Log parsing` `SIEM concepts`

## Prerequisites

### System Requirements

- Python 3.10+
- Linux system with **systemd** (required for `journalctl`)
- Docker and Docker Compose (for Elasticsearch + Grafana stack)
- User must belong to the `systemd-journal` group

```bash
# Install Docker and Docker Compose (Arch/Garuda)
sudo pacman -S docker docker-compose

# Start and enable Docker
sudo systemctl enable --now docker

# Add your user to docker group (avoid sudo for docker commands)
sudo usermod -aG docker $USER
# Log out and back in for this to take effect

# Install Python dependencies
source venv/bin/activate
pip install -r requirements.txt
```

### Grant journalctl Access Without sudo

By default, reading systemd journals requires root. Add yourself to the `systemd-journal` group:

```bash
sudo usermod -aG systemd-journal $USER
# Log out and back in, then verify:
journalctl -n 5   # should work without sudo
```

### System Tool Dependencies

```bash
# Arch/Garuda
sudo pacman -S docker docker-compose

# Verify journalctl access
journalctl -n 5   # Should show logs without sudo
```

## Project Structure

```
03-simple-siem/
├── src/
│   ├── main.py              # Entry point with CLI sub-commands
│   └── siem/
│       ├── journal_reader.py   # Read logs via journalctl (JSON output)
│       ├── storage.py           # SQLite: init, save, query, deduplication
│       ├── detection.py         # Brute-force and SSH login detection
│       ├── display.py           # Pretty-print results in tables
│       └── es_indexer.py       # Elasticsearch bulk indexer + alert index
├── docker/
│   └── docker-compose.yml       # Elasticsearch 8.13 + Grafana 10.4 stack
├── db/
│   └── .gitkeep                   # SQLite database stored here
└── README.md
```

## Installation

```bash
# 1. Clone repository and setup venv (from project root)
cd /path/to/Network-Security-Projects
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Grant journal access (one-time)
sudo usermod -aG systemd-journal $USER
# Log out and back in

# 3. Start Docker stack (Elasticsearch + Grafana)
cd level-1-beginner/03-simple-siem/docker
docker compose up -d

# 4. Verify services
docker ps | grep siem
curl http://localhost:9200   # Elasticsearch
curl http://localhost:3000  # Grafana
```

## All CLI Sub-Commands

| Command | Description | Key Arguments |
|---|---|---|
| `collect` | Collect logs from journalctl | `--minutes`, `--priority`, `--limit`, `--save` |
| `detect` | Detect anomalies from stored logs | `--sudo-threshold` |
| `index` | Push logs from SQLite to Elasticsearch | *(none)* |
| `alerts` | Run detection and push alerts to Elasticsearch | `--sudo-threshold` |
| `pipeline` | Full pipeline: collect → save → index → detect → alert | `--minutes`, `--sudo-threshold` |

### `collect` Arguments

| Argument | Default | Description |
|---|---|---|
| `--minutes` | 10 | How many minutes back to collect logs |
| `--priority` | *(all)* | Filter by syslog priority: `err`, `warning`, `info`, etc. |
| `--limit` | 30 | Max log entries to display in terminal |
| `--save` | *(off)* | Save collected logs to SQLite database |

### `detect` / `alerts` / `pipeline` Arguments

| Argument | Default | Description |
|---|---|---|
| `--sudo-threshold` | 3 | Number of failed sudo attempts to flag as brute-force |

## Usage

### Basic Workflow

```bash
# Activate venv
source venv/bin/activate

# Collect logs from the last 60 minutes and save to SQLite
venv/bin/python src/main.py collect --minutes 60 --save

# View only error/warning logs (no save)
venv/bin/python src/main.py collect --minutes 30 --priority err

# Detect anomalous behavior from stored logs
venv/bin/python src/main.py detect --sudo-threshold 3

# Push logs to Elasticsearch (for Grafana)
venv/bin/python src/main.py index

# Run detection and push alerts to Elasticsearch
venv/bin/python src/main.py alerts --sudo-threshold 3
```

### Full Pipeline (One Command)

```bash
# Collect → Save → Index → Detect → Alert (all in one)
venv/bin/python src/main.py pipeline --minutes 60 --sudo-threshold 3
```

### Docker Stack Management

```bash
# Start Elasticsearch + Grafana
cd docker && docker compose up -d

# Stop services
cd docker && docker compose down

# View logs
docker compose logs -f

# Reset volumes (delete all data)
docker compose down -v
```

## Grafana Dashboard Setup

### 1. Access Grafana

Open http://localhost:3000 in your browser
Login: `admin` / `admin`

### 2. Add Elasticsearch Data Source

1. Click **Configuration** (gear icon) → **Data Sources**
2. Click **Add data source**
3. Select **Elasticsearch**
4. Configure:
   - **URL**: `http://siem-elasticsearch:9200`
   - **Index name**: `siem-logs`
   - **Time field**: `timestamp`
   - **Version**: `8.x`
5. Click **Save & Test**

### 3. Create Dashboard Panels

Create a new dashboard and add panels:

- **Log Volume Over Time**: Time series, count by `@timestamp`
- **Priority Distribution**: Pie chart grouped by `priority_label`
- **Top Active Units**: Table showing `unit` with document count
- **Recent Logs**: Table sorted by `@timestamp` descending, showing `message`

### 4. Add Alert Data Source (for alerts)

Add another data source for `siem-alerts` index with the same configuration.

## Verified Results

✅ **Successfully collected and stored system logs**
- Accurate log normalization with priority mapping
- Successful deduplication on repeated runs
- Detected simulated sudo brute-force attempts
- Correctly identified failed SSH login patterns
- Logs indexed to Elasticsearch without data loss
- Grafana panels displaying real-time log data

## Technical Notes

- **Journalctl format**: Uses `-o json` output which provides structured data — no regex parsing needed.
- **Syslog priorities**: 0=EMERG, 1=ALERT, 2=CRIT, 3=ERR, 4=WARNING, 5=NOTICE, 6=INFO, 7=DEBUG.
- **Deduplication logic**: Based on `(timestamp, pid, message)` tuple to avoid storing duplicate logs on repeated runs.
- **Elasticsearch deduplication**: Uses SQLite row `id` as Elasticsearch `_id` to prevent re-indexing on pipeline re-runs.
- **Alert severity**: HIGH if ≥10 failed attempts, MEDIUM otherwise.

## Troubleshooting

### "journalctl: command not found"
Your system does not use systemd. This project requires a systemd-based Linux distribution (Arch, Ubuntu 16.04+, Fedora, etc.).

### "Permission denied" on journalctl
You need to be in the `systemd-journal` group:
```bash
sudo usermod -aG systemd-journal $USER
```
Then log out and back in.

### Elasticsearch container fails to start
Increase virtual memory on the host:
```bash
sudo sysctl -w vm.max_map_count=262144
```
Make it permanent:
```bash
echo "vm.max_map_count=262144" | sudo tee -a /etc/sysctl.conf
```

### "No logs in SQLite" when running index
Run `collect --save` first. The `index` command reads from the SQLite database populated by `collect --save`.

### Port 9200 or 3000 already in use
Stop conflicting services or check what's using the port:
```bash
sudo lsof -i :9200
sudo lsof -i :3000
```

## References

- [systemd Journal Documentation](https://www.freedesktop.org/software/systemd/man/journalctl.html)
- [Elasticsearch 8.x Reference](https://www.elastic.co/guide/en/elasticsearch/reference/8.13/)
- [Grafana Documentation](https://grafana.com/docs/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)

<p align="right">

⬆️ <a href="#language">Back to Language Selection</a>

</p>

---

<a id="tieng-viet"></a>

# 🇻🇳 Tiếng Việt

# 📊 03 - Simple SIEM

## Mô tả

Thu thập log hệ thống Linux qua `journalctl`, lưu trữ vào SQLite, phát hiện hành vi bất thường (tấn công brute-force), và trực quan hóa dữ liệu bằng Elasticsearch và dashboard Grafana.

## Tính năng

- [x] Thu thập log qua journalctl (định dạng JSON — không cần regex)
- [x] Chuẩn hóa log thành format thống nhất
- [x] Lưu vào SQLite với logic dedup (tránh lưu trùng)
- [x] Truy vấn log theo priority và unit
- [x] Phát hiện tấn công sudo brute-force (nhiều lần nhập sai password)
- [x] Phát hiện các lần SSH login thất bại
- [x] Đẩy log lên Elasticsearch (bulk indexing với dedup qua SQLite ID)
- [x] Đẩy alerts lên Elasticsearch index riêng cho dashboard cảnh báo
- [x] Dashboard Grafana: Log Volume, Priority Distribution, Top Units, Recent Logs

## Kỹ năng thực hành

`Python` `Linux systemd/journald` `SQLite` `Elasticsearch` `Grafana` `Docker Compose` `Log parsing` `SIEM concepts`

## Yêu cầu hệ thống

### Yêu cầu

- Python 3.10+
- Hệ thống Linux có **systemd** (cần cho journalctl)
- Docker và Docker Compose (để chạy Elasticsearch + Grafana)
- User phải thuộc group `systemd-journal`

```bash
# Cài đặt Docker và Docker Compose (Arch/Garuda)
sudo pacman -S docker docker-compose

# Khởi động và bật Docker
sudo systemctl enable --now docker

# Thêm user vào docker group (khỏi cần sudo cho docker)
sudo usermod -aG docker $USER
# Log out và login lại để áp dụng

# Cài đặt Python dependencies
source venv/bin/activate
pip install -r requirements.txt
```

### Cấp quyền truy cập journalctl không cần sudo

Mặc định, đọc systemd journal cần root. Thêm user vào group `systemd-journal`:

```bash
sudo usermod -aG systemd-journal $USER
# Log out và login lại, sau đó kiểm tra:
journalctl -n 5   # Nên hoạt động không cần sudo
```

### Dependencies cho hệ thống

```bash
# Arch/Garuda
sudo pacman -S docker docker-compose

# Kiểm tra truy cập journalctl
journalctl -n 5   # Hiển thị logs không cần sudo
```

## Cấu trúc dự án

```
03-simple-siem/
├── src/
│   ├── main.py              # Entry point với CLI sub-commands
│   └── siem/
│       ├── journal_reader.py   # Đọc log qua journalctl (output JSON)
│       ├── storage.py           # SQLite: init, save, query, deduplication
│       ├── detection.py         # Brute-force và SSH login detection
│       ├── display.py           # Pretty-print kết quả dạng bảng
│       └── es_indexer.py       # Elasticsearch bulk indexer + alert index
├── docker/
│   └── docker-compose.yml       # Elasticsearch 8.13 + Grafana 10.4 stack
├── db/
│   └── .gitkeep                   # SQLite database lưu ở đây
└── README.md
```

## Cài đặt

```bash
# 1. Clone repo và setup venv (từ thư mục gốc)
cd /path/to/Network-Security-Projects
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Cấp quyền truy cập journal (một lần)
sudo usermod -aG systemd-journal $USER
# Log out và login lại

# 3. Khởi động Docker stack (Elasticsearch + Grafana)
cd level-1-beginner/03-simple-siem/docker
docker compose up -d

# 4. Kiểm tra dịch vụ
docker ps | grep siem
curl http://localhost:9200   # Elasticsearch
curl http://localhost:3000  # Grafana
```

## Tất cả CLI Sub-Commands

| Command | Mô tả | Đối số quan trọng |
|---|---|---|
| `collect` | Thu thập log từ journalctl | `--minutes`, `--priority`, `--limit`, `--save` |
| `detect` | Phát hiện bất thường từ log đã lưu | `--sudo-threshold` |
| `index` | Đẩy log từ SQLite lên Elasticsearch | *(không có)* |
| `alerts` | Chạy detection và đẩy alerts lên Elasticsearch | `--sudo-threshold` |
| `pipeline` | Full pipeline: collect → save → index → detect → alert | `--minutes`, `--sudo-threshold` |

### Đối số của `collect`

| Đối số | Mặc định | Mô tả |
|---|---|---|
| `--minutes` | 10 | Số phút gần đây cần thu thập log |
| `--priority` | *(tất cả)* | Lọc theo mức syslog: `err`, `warning`, `info`, v.v. |
| `--limit` | 30 | Số dòng log hiển thị tối đa |
| `--save` | *(tắt)* | Lưu log thu thập được vào SQLite |

### Đối số của `detect` / `alerts` / `pipeline`

| Đối số | Mặc định | Mô tả |
|---|---|---|
| `--sudo-threshold` | 3 | Số lần nhập sai sudo để báo cáo là brute-force |

## Cách chạy

### Workflow cơ bản

```bash
# Activate venv
source venv/bin/activate

# Thu thập log 60 phút gần đây và lưu vào SQLite
venv/bin/python src/main.py collect --minutes 60 --save

# Chỉ xem log lỗi/cảnh báo, không lưu
venv/bin/python src/main.py collect --minutes 30 --priority err

# Phát hiện bất thường từ log đã lưu
venv/bin/python src/main.py detect --sudo-threshold 3

# Đẩy log lên Elasticsearch (cho Grafana)
venv/bin/python src/main.py index

# Chạy detection và đẩy alerts lên Elasticsearch
venv/bin/python src/main.py alerts --sudo-threshold 3
```

### Full Pipeline (Một lệnh duy nhất)

```bash
# Collect → Save → Index → Detect → Alert (tất cả trong một lệnh)
venv/bin/python src/main.py pipeline --minutes 60 --sudo-threshold 3
```

### Quản lý Docker Stack

```bash
# Khởi động Elasticsearch + Grafana
cd docker && docker compose up -d

# Dừng dịch vụ
cd docker && docker compose down

# Xem logs
docker compose logs -f

# Reset volumes (xóa tất cả data)
docker compose down -v
```

## Cài đặt Dashboard Grafana

### 1. Truy cập Grafana

Mở http://localhost:3000 trong trình duyệt
Đăng nhập: `admin` / `admin`

### 2. Thêm Elasticsearch Data Source

1. Click **Configuration** (biểu tượng bánh răng) → **Data Sources**
2. Click **Add data source**
3. Chọn **Elasticsearch**
4. Cấu hình:
   - **URL**: `http://siem-elasticsearch:9200`
   - **Index name**: `siem-logs`
   - **Time field**: `timestamp`
   - **Version**: `8.x`
5. Click **Save & Test**

### 3. Tạo Dashboard Panels

Tạo dashboard mới và thêm các panels:

- **Log Volume Over Time**: Time series, count theo `@timestamp`
- **Priority Distribution**: Biểu đồ tròn theo `priority_label`
- **Top Active Units**: Bảng hiển thị `unit` với số lượng document
- **Recent Logs**: Bảng sắp xếp theo `@timestamp` giảm dần, hiển thị `message`

### 4. Thêm Alert Data Source (cho alerts)

Thêm data source khác cho index `siem-alerts` với cùng cấu hình.

## Kết quả đã kiểm chứng

✅ **Đã thu thập và lưu trữ log hệ thống thành công**
- Chuẩn hóa log chính xác với ánh xạ priority
- Deduplication thành công khi chạy lại
- Phát hiện các nỗ lực sudo brute-force mô phỏng
- Xác định đúng các mẫu SSH login thất bại
- Log được đẩy lên Elasticsearch không mất dữ liệu
- Các panel Grafana hiển thị log data theo thời gian thực

## Ghi chú kỹ thuật

- **Định dạng journalctl**: Sử dụng output `-o json` cung cấp dữ liệu có cấu trúc — không cần regex.
- **Syslog priorities**: 0=EMERG, 1=ALERT, 2=CRIT, 3=ERR, 4=WARNING, 5=NOTICE, 6=INFO, 7=DEBUG.
- **Deduplication logic**: Dựa trên tuple `(timestamp, pid, message)` để tránh lưu trùng log khi chạy lại.
- **Elasticsearch deduplication**: Sử dụng `id` từ SQLite làm `_id` trong Elasticsearch để tránh re-index khi chạy lại pipeline.
- **Alert severity**: HIGH nếu ≥10 lần thất bại, MEDIUM cho các trường hợp khác.

## Xử lý sự cố

### "journalctl: command not found"
Hệ thống không dùng systemd. Dự án này yêu cầu Linux distribution dựa trên systemd (Arch, Ubuntu 16.04+, Fedora, v.v.).

### "Permission denied" khi chạy journalctl
Cần thuộc group `systemd-journal`:
```bash
sudo usermod -aG systemd-journal $USER
```
Sau đó log out và login lại.

### Container Elasticsearch không khởi động được
Tăng virtual memory trên host:
```bash
sudo sysctl -w vm.max_map_count=262144
```
Lưu vĩnh viễn:
```bash
echo "vm.max_map_count=262144" | sudo tee -a /etc/sysctl.conf
```

### "No logs in SQLite" khi chạy index
Chạy `collect --save` trước. Lệnh `index` đọc từ SQLite database đã được populate bởi `collect --save`.

### Port 9200 hoặc 3000 đã được sử dụng
Dừng các dịch vụ xung đột hoặc kiểm tra port:
```bash
sudo lsof -i :9200
sudo lsof -i :3000
```

## Tham khảo

- [systemd Journal Documentation](https://www.freedesktop.org/software/systemd/man/journalctl.html)
- [Elasticsearch 8.x Reference](https://www.elastic.co/guide/en/elasticsearch/reference/8.13/)
- [Grafana Documentation](https://grafana.com/docs/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)

<p align="right">

⬆️ <a href="#language">Quay lại chọn ngôn ngữ</a>

</p>