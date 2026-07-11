# 🛡️ Dự án Bảo mật Mạng

**Language / Ngôn ngữ:** [English](README.md) | [Tiếng Việt](README.vi.md)

> Lab thực hành Blue Team / SOC / NOC — tự xây dựng từ đầu trên Linux

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://python.org)
[![Linux](https://img.shields.io/badge/OS-Garuda%20Linux-5DA2D5?logo=linux&logoColor=white)](https://garudalinux.org)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)](https://docker.com)
[![Elasticsearch](https://img.shields.io/badge/Elasticsearch-8.13-005571?logo=elasticsearch)](https://elastic.co)
[![Grafana](https://img.shields.io/badge/Grafana-10.4-F46800?logo=grafana&logoColor=white)](https://grafana.com)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## 🎯 Giới thiệu

Tôi xây dựng repo này để thực hành các kỹ năng **Blue Team / SOC Analyst**
thông qua các dự án thực tế, viết từ đầu bằng Python trên môi trường Linux thật.
Không dùng công cụ hộp đen — tự implement từng tính năng để hiểu nguyên lý.

**Kỹ năng thực hành:**
- Phân tích traffic mạng và phát hiện tấn công từ file `.pcap`
- Quét mạng LAN, nhận diện OS qua TTL fingerprint
- Thu thập, parse, lưu trữ và trực quan hóa log hệ thống
- Xây dựng SIEM stack với Elasticsearch + Grafana

---

## 🗂️ Danh sách dự án

| # | Dự án | Mô tả | Công nghệ | Trạng thái |
|---|-------|--------|-----------|------------|
| 01 | [🔍 Traffic Analyzer](level-1-beginner/01-traffic-analyzer/) | Phân tích `.pcap`, phát hiện SYN flood / Port scan / Ping sweep | Python, Scapy, tcpdump | ✅ Hoàn thành |
| 02 | [📡 Network Scanner](level-1-beginner/02-network-scanner/) | Quét LAN, ARP scan, nhận diện OS qua TTL, scan port, xuất CSV/JSON | Python, Scapy, Nmap | ✅ Hoàn thành |
| 03 | [📊 Simple SIEM](level-1-beginner/03-simple-siem/) | Thu thập log, lưu SQLite, phát hiện brute-force, dashboard Grafana | Python, SQLite, Elasticsearch, Grafana, Docker | ✅ Hoàn thành |
| - | ⭐⭐ Trung cấp | *(Sắp ra mắt)* | - | 🔒 |
| - | ⭐⭐⭐ Nâng cao | *(Sắp ra mắt)* | - | 🔒 |

---

## ⚙️ Cài đặt

### Dependencies hệ thống (Arch/Garuda Linux)

```bash
sudo pacman -S nmap tcpdump tshark wireshark-qt docker docker-compose python python-pip
```

### Khởi động và bật Docker

```bash
sudo systemctl enable --now docker
sudo usermod -aG docker $USER
# Log out và login lại
```

### Setup Python Virtual Environment

```bash
git clone git@github.com:Azynora/Network-Security-Projects.git
cd Network-Security-Projects

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Cấp quyền truy cập Journal (cho Dự án 03 - SIEM)

```bash
sudo usermod -aG systemd-journal $USER
# Log out và login lại
```

## 🚀 Chạy nhanh

### Dự án 01 - Traffic Analyzer

```bash
# Phân tích file .pcap
venv/bin/python level-1-beginner/01-traffic-analyzer/src/main.py path/to/capture.pcap

# Với ngưỡng phát hiện tùy chỉnh
venv/bin/python level-1-beginner/01-traffic-analyzer/src/main.py samples/attack_test.pcap \
    --syn-threshold 20 \
    --port-threshold 15 \
    --ping-threshold 10
```

### Dự án 02 - Network Scanner

```bash
# ARP scan + OS fingerprint (nhanh)
sudo venv/bin/python level-1-beginner/02-network-scanner/src/main.py 192.168.1.0/24

# Với port scan (chậm hơn, đầy đủ hơn)
sudo venv/bin/python level-1-beginner/02-network-scanner/src/main.py 192.168.1.0/24 --ports
```

### Dự án 03 - Simple SIEM

```bash
# 1. Khởi động Docker stack (Elasticsearch + Grafana)
cd level-1-beginner/03-simple-siem/docker && docker compose up -d
cd ../../..

# 2. Thu thập log và lưu vào SQLite
venv/bin/python level-1-beginner/03-simple-siem/src/main.py collect --minutes 60 --save

# 3. Đẩy log lên Elasticsearch
venv/bin/python level-1-beginner/03-simple-siem/src/main.py index

# 4. Phát hiện bất thường
venv/bin/python level-1-beginner/03-simple-siem/src/main.py detect --sudo-threshold 3

# 5. HOẶC chạy full pipeline trong một lệnh
venv/bin/python level-1-beginner/03-simple-siem/src/main.py pipeline --minutes 60 --sudo-threshold 3

# 6. Xem Grafana dashboard → http://localhost:3000 (admin/admin)
```

## 📁 Cấu trúc dự án

```
Network-Security-Projects/
├── level-1-beginner/
│   ├── 01-traffic-analyzer/
│   │   ├── src/
│   │   │   ├── main.py
│   │   │   └── analyzer/
│   │   │       ├── loader.py      # đọc .pcap
│   │   │       ├── stats.py       # top talkers/ports/protocols
│   │   │       ├── detection.py   # SYN flood, port scan, ping sweep
│   │   │       └── display.py     # hiển thị bảng rich
│   │   ├── samples/               # file .pcap mẫu
│   │   ├── docs/                  # ảnh chụp và tài liệu
│   │   └── README.md              # song ngữ (EN + VI)
│   ├── 02-network-scanner/
│   │   ├── src/
│   │   │   ├── main.py
│   │   │   └── scanner/
│   │   │       ├── arp.py         # ARP scan
│   │   │       ├── fingerprint.py # nhận diện OS qua TTL
│   │   │       ├── ports.py       # port scan bằng nmap
│   │   │       ├── lookup.py      # hostname + MAC vendor
│   │   │       ├── display.py     # hiển thị bảng rich
│   │   │       └── exporter.py    # xuất CSV/JSON
│   │   ├── docs/                  # ảnh chụp và tài liệu
│   │   └── README.md              # song ngữ (EN + VI)
│   └── 03-simple-siem/
│       ├── src/
│       │   ├── main.py
│       │   └── siem/
│       │       ├── journal_reader.py  # thu thập log qua journalctl
│       │       ├── storage.py         # SQLite
│       │       ├── detection.py       # phát hiện brute-force
│       │       ├── display.py         # hiển thị kết quả
│       │       └── es_indexer.py      # đẩy log lên Elasticsearch
│       ├── docker/
│       │   └── docker-compose.yml     # ES + Grafana stack
│       └── README.md                  # song ngữ (EN + VI)
├── requirements.txt
└── resources/
```

---

## 🛠️ Công cụ sử dụng

| Công cụ | Mục đích | Dự án |
|---------|----------|-------|
| **Scapy** | Tạo packet và parse .pcap | 01, 02 |
| **tcpdump** | Bắt traffic mạng | 01 |
| **nmap** | Quét port | 02 |
| **Nping** | Tạo traffic tấn công test | 01 |
| **Wireshark/tshark** | Phân tích giao thức mạng | 01 |
| **journalctl** | Đọc log systemd | 03 |
| **SQLite** | Lưu trữ log | 03 |
| **Elasticsearch** | Đánh index và tìm kiếm log | 03 |
| **Grafana** | Trực quan hóa log dashboard | 03 |
| **Docker Compose** | Triển khai SIEM stack | 03 |

---

## ⚠️ Tuyên bố miễn trách

> Các công cụ trong repo này **chỉ dùng cho mục đích học tập** trong môi trường
> lab hoặc mạng được cấp phép. Nghiêm cấm sử dụng trên hệ thống không thuộc quyền sở hữu.

---

## 📚 Tài liệu

Mỗi dự án có README riêng chi tiết với:
- Hướng dẫn cài đặt đầy đủ
- Tất cả argument dòng lệnh
- Hướng dẫn sử dụng từng bước
- Mẹo xử lý sự cố
- Ghi chú kỹ thuật và tham khảo

**README các dự án:**
- [01 - Traffic Analyzer](level-1-beginner/01-traffic-analyzer/README.md)
- [02 - Network Scanner](level-1-beginner/02-network-scanner/README.md)
- [03 - Simple SIEM](level-1-beginner/03-simple-siem/README.md)

---

## 🔗 Tham khảo

- [Tài liệu Scapy](https://scapy.net/)
- [Hướng dẫn Nmap](https://nmap.org/book/man.html)
- [systemd Journal Documentation](https://www.freedesktop.org/software/systemd/man/journalctl.html)
- [Elasticsearch 8.x Reference](https://www.elastic.co/guide/en/elasticsearch/reference/8.13/)
- [Grafana Documentation](https://grafana.com/docs/)
- [TCP/IP Illustrated, Volume 1](https://www.amazon.com/dp/0201533487)