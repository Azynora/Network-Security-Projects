# 🛡️ Network Security Projects

> Hands-on practice lab — Blue Team | SOC | NOC | System Admin

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Linux](https://img.shields.io/badge/OS-Linux-FCC624?logo=linux&logoColor=black)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🎯 Mục tiêu

Xây dựng các công cụ thực tế từ đầu để luyện kỹ năng:
- Phân tích network traffic & phát hiện tấn công
- Thu thập, parse và visualize log (SIEM đơn giản)
- Quét mạng và phát hiện tài sản (Asset Discovery)

---

## 🗂️ Cấu trúc dự án

| # | Level | Dự án | Công nghệ | Status |
|---|-------|--------|-----------|--------|
| 01 | ⭐ Beginner | [Traffic Analyzer](level-1-beginner/01-traffic-analyzer/) | Python, Scapy, Tshark | 🚧 In Progress |
| 02 | ⭐ Beginner | [Network Scanner](level-1-beginner/02-network-scanner/) | Python, Nmap, ARP | 📅 Planned |
| 03 | ⭐ Beginner | [Simple SIEM](level-1-beginner/03-simple-siem/) | ELK, Grafana, Docker | 📅 Planned |
| - | ⭐⭐ Intermediate | *(Coming soon)* | - | 🔒 Locked |
| - | ⭐⭐⭐ Advanced | *(Coming soon)* | - | 🔒 Locked |

---

## ⚙️ Thiết lập môi trường

```bash
git clone git@github.com:your-username/Network-Security-Projects.git
cd Network-Security-Projects
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 🔧 Yêu cầu hệ thống

- OS: Linux (Garuda / Arch / Ubuntu)
- Python: 3.10+
- Docker + Docker Compose
- Wireshark / Tshark / Nmap

---

## ⚠️ Disclaimer

> Các công cụ trong repo này **chỉ dùng cho mục đích học tập** trong
> môi trường lab hoặc mạng được cấp phép. Nghiêm cấm sử dụng trái phép.
