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

```bash
git clone git@github.com:Azynora/Network-Security-Projects.git
cd Network-Security-Projects

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Công cụ hệ thống (Arch/Garuda)
sudo pacman -S nmap tshark tcpdump wireshark-qt
```

## 🚀 Chạy nhanh

```bash
# 02 - Network Scanner
sudo venv/bin/python level-1-beginner/02-network-scanner/src/main.py 192.168.1.0/24 --ports

# 01 - Traffic Analyzer
venv/bin/python level-1-beginner/01-traffic-analyzer/src/main.py path/to/capture.pcap

# 03 - Simple SIEM (cần Docker)
cd level-1-beginner/03-simple-siem/docker && docker compose up -d
cd ../.. && venv/bin/python level-1-beginner/03-simple-siem/src/main.py collect --minutes 60 --save
venv/bin/python level-1-beginner/03-simple-siem/src/main.py index
venv/bin/python level-1-beginner/03-simple-siem/src/main.py detect
# Grafana dashboard → http://localhost:3000
```

---

## 📁 Cấu trúc dự án

```
Network-Security-Projects/
├── level-1-beginner/
│   ├── 01-traffic-analyzer/
│   │   └── src/
│   │       ├── main.py
│   │       └── analyzer/
│   │           ├── loader.py      # đọc file .pcap
│   │           ├── stats.py       # top talkers/ports/protocols
│   │           ├── detection.py   # phát hiện SYN flood, port scan, ping sweep
│   │           └── display.py     # hiển thị bảng rich
│   ├── 02-network-scanner/
│   │   └── src/
│   │       ├── main.py
│   │       └── scanner/
│   │           ├── arp.py         # ARP scan
│   │           ├── fingerprint.py # nhận diện OS qua TTL
│   │           ├── ports.py       # port scan bằng nmap
│   │           ├── lookup.py      # hostname + MAC vendor
│   │           ├── display.py     # hiển thị bảng rich
│   │           └── exporter.py    # xuất CSV/JSON
│   └── 03-simple-siem/
│       ├── src/
│       │   ├── main.py
│       │   └── siem/
│       │       ├── journal_reader.py  # thu thập log qua journalctl
│       │       ├── storage.py         # SQLite
│       │       ├── detection.py       # phát hiện brute-force
│       │       ├── display.py         # hiển thị kết quả
│       │       └── es_indexer.py      # đẩy log lên Elasticsearch
│       └── docker/
│           └── docker-compose.yml     # ES + Grafana stack
├── requirements.txt
└── resources/
```
---

## ⚠️ Tuyên bố miễn trách

> Các công cụ trong repo này **chỉ dùng cho mục đích học tập** trong môi trường
> lab hoặc mạng được cấp phép. Nghiêm cấm sử dụng trên hệ thống không thuộc quyền sở hữu.
