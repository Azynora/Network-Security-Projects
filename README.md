# 🛡️ Network Security Projects

**Language / Ngôn ngữ:** [English](README.md) | [Tiếng Việt](README.vi.md)

> Hands-on Blue Team / SOC / NOC practice lab — built from scratch on Linux

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://python.org)
[![Linux](https://img.shields.io/badge/OS-Garuda%20Linux-5DA2D5?logo=linux&logoColor=white)](https://garudalinux.org)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)](https://docker.com)
[![Elasticsearch](https://img.shields.io/badge/Elasticsearch-8.13-005571?logo=elasticsearch)](https://elastic.co)
[![Grafana](https://img.shields.io/badge/Grafana-10.4-F46800?logo=grafana&logoColor=white)](https://grafana.com)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## 🎯 About

I built this repository to practice **Blue Team / SOC Analyst** skills through
real-world projects written from scratch in Python on a real Linux environment.
No black-box tools — every feature is implemented manually to understand the
underlying principles.

**Skills practiced:**
- Network traffic analysis and attack detection from `.pcap` files
- LAN scanning, OS fingerprinting via TTL
- Collecting, parsing, storing and visualizing system logs
- Building a SIEM stack with Elasticsearch + Grafana

---

## 🗂️ Projects

| # | Project | Description | Stack | Status |
|---|---------|-------------|-------|--------|
| 01 | [🔍 Traffic Analyzer](level-1-beginner/01-traffic-analyzer/) | Analyze `.pcap` files, detect SYN flood / Port scan / Ping sweep | Python, Scapy, tcpdump | ✅ Done |
| 02 | [📡 Network Scanner](level-1-beginner/02-network-scanner/) | LAN scan, ARP, OS fingerprint via TTL, port scan, CSV/JSON export | Python, Scapy, Nmap | ✅ Done |
| 03 | [📊 Simple SIEM](level-1-beginner/03-simple-siem/) | Log collection, SQLite storage, brute-force detection, Grafana dashboard | Python, SQLite, Elasticsearch, Grafana, Docker | ✅ Done |
| - | ⭐⭐ Intermediate | *(Coming soon)* | - | 🔒 |
| - | ⭐⭐⭐ Advanced | *(Coming soon)* | - | 🔒 |

---

## ⚙️ Installation

### System Dependencies (Arch/Garuda Linux)

```bash
sudo pacman -S nmap tcpdump tshark wireshark-qt docker docker-compose python python-pip
```

### Start and Enable Docker

```bash
sudo systemctl enable --now docker
sudo usermod -aG docker $USER
# Log out and back in
```

### Setup Python Virtual Environment

```bash
git clone git@github.com:Azynora/Network-Security-Projects.git
cd Network-Security-Projects

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Grant Journal Access (for Project 03 - SIEM)

```bash
sudo usermod -aG systemd-journal $USER
# Log out and back in
```

## 📁 Project Structure

```
Network-Security-Projects/
├── level-1-beginner/
│   ├── 01-traffic-analyzer/
│   │   ├── src/
│   │   │   ├── main.py
│   │   │   └── analyzer/
│   │   │       ├── loader.py      # read .pcap
│   │   │       ├── stats.py       # top talkers/ports/protocols
│   │   │       ├── detection.py   # SYN flood, port scan, ping sweep
│   │   │       └── display.py     # rich table output
│   │   ├── samples/               # sample .pcap files
│   │   ├── docs/                  # screenshots and documentation
│   │   └── README.md              # bilingual (EN + VI)
│   ├── 02-network-scanner/
│   │   ├── src/
│   │   │   ├── main.py
│   │   │   └── scanner/
│   │   │       ├── arp.py         # ARP scan
│   │   │       ├── fingerprint.py # OS detect via TTL
│   │   │       ├── ports.py       # nmap port scan
│   │   │       ├── lookup.py      # hostname + MAC vendor
│   │   │       ├── display.py     # rich table output
│   │   │       └── exporter.py    # CSV/JSON export
│   │   ├── docs/                  # screenshots and documentation
│   │   └── README.md              # bilingual (EN + VI)
│   └── 03-simple-siem/
│       ├── src/
│       │   ├── main.py
│       │   └── siem/
│       │       ├── journal_reader.py  # journalctl collector
│       │       ├── storage.py         # SQLite
│       │       ├── detection.py       # brute-force detection
│       │       ├── display.py         # rich output
│       │       └── es_indexer.py      # Elasticsearch indexer
│       ├── docker/
│       │   └── docker-compose.yml     # ES + Grafana stack
│       └── README.md                  # bilingual (EN + VI)
├── requirements.txt
└── resources/
```

---

## 🛠️ Tools Used

| Tool | Purpose | Project |
|------|---------|---------|
| **Scapy** | Packet crafting and .pcap parsing | 01, 02 |
| **tcpdump** | Capture network traffic | 01 |
| **nmap** | Port scanning | 02 |
| **Nping** | Generate test attack traffic | 01 |
| **Wireshark/tshark** | Network protocol analysis | 01 |
| **journalctl** | Read systemd logs | 03 |
| **SQLite** | Log storage | 03 |
| **Elasticsearch** | Log indexing and search | 03 |
| **Grafana** | Log visualization dashboards | 03 |
| **Docker Compose** | SIEM stack deployment | 03 |

---

## ⚠️ Disclaimer

> Tools in this repository are **for educational purposes only**, in a lab
> environment or on networks you own and have permission to test.
> Do not use on unauthorized systems.

---

## 📚 Documentation

Each project has its own detailed README with:
- Complete installation instructions
- All command-line arguments documented
- Step-by-step usage guides
- Troubleshooting tips
- Technical notes and references

**Individual project READMEs:**
- [01 - Traffic Analyzer](level-1-beginner/01-traffic-analyzer/README.md)
- [02 - Network Scanner](level-1-beginner/02-network-scanner/README.md)
- [03 - Simple SIEM](level-1-beginner/03-simple-siem/README.md)

---

## 🔗 References

- [Scapy Documentation](https://scapy.net/)
- [Nmap Reference Guide](https://nmap.org/book/man.html)
- [systemd Journal Documentation](https://www.freedesktop.org/software/systemd/man/journalctl.html)
- [Elasticsearch 8.x Reference](https://www.elastic.co/guide/en/elasticsearch/reference/8.13/)
- [Grafana Documentation](https://grafana.com/docs/)
- [TCP/IP Illustrated, Volume 1](https://www.amazon.com/dp/0201533487)
