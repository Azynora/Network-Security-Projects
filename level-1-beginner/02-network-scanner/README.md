<a id="language"></a>

<div align="right">

## 🌐 Language

🇺🇸 [English](#english) | 🇻🇳 [Tiếng Việt](#tieng-viet)

</div>

---

<a id="english"></a>

# 🇺🇸 English

# 🔍 02 - Network Scanner — Asset Discovery

## Description

Scan LAN networks, discover online devices, detect operating systems, and scan open ports. This tool performs comprehensive network asset discovery using ARP scans, TTL-based OS fingerprinting, and Nmap port scanning.

## Features

- [x] ARP scan to discover online LAN devices
- [x] Hostname resolution via reverse DNS
- [x] MAC vendor lookup (IEEE OUI database)
- [x] OS fingerprinting via TTL (Linux/Windows/Network device)
- [x] Port scan (optional) using Nmap TCP connect scan
- [x] Rich table output with colorized formatting
- [x] CSV and JSON report export with timestamps
- [x] Progress indicators during scanning

## Skills Practiced

`Python` `Scapy` `Nmap` `ARP` `Socket` `TTL Fingerprinting` `Asset Discovery`

## Installation

```bash
# System dependencies (Arch/Garuda)
sudo pacman -S nmap tshark wireshark-qt

# Python dependencies
pip install scapy python-nmap rich
```

## Usage

```bash
# Activate venv first
source venv/bin/activate

# ARP scan + OS fingerprint only (fast)
sudo venv/bin/python src/main.py 192.168.1.0/24

# With port scan (slower, complete)
sudo venv/bin/python src/main.py 192.168.1.0/24 --ports

# Full port range (slow, comprehensive)
sudo venv/bin/python src/main.py 192.168.1.0/24 --ports --port-range 1-65535
```

### Command Line Arguments

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `target` | positional | required | IP range to scan, e.g. `192.168.1.0/24` |
| `--ports` | flag | false | Enable port scanning (requires Nmap) |
| `--port-range` | string | `1-1000` | Port range to scan, e.g. `1-65535` |

### Permissions

⚠️ This tool **requires `sudo`** because it creates raw sockets for ARP and ICMP packets.

## Project Structure

```
02-network-scanner/
├── src/
│   ├── main.py                  # Entry point with CLI
│   └── scanner/
│       ├── arp.py               # ARP scan for device discovery
│       ├── fingerprint.py        # OS detection via TTL
│       ├── ports.py              # Nmap port scanning
│       ├── lookup.py             # DNS resolution + MAC vendor
│       ├── display.py            # Rich table output
│       └── exporter.py           # CSV/JSON report generation
├── docs/
│   └── screenshots/              # Scan result screenshots
└── README.md
```

## Output

Results are saved to `output/reports/` as CSV and JSON with timestamps.

### Example CSV Output:
```
ip,mac,hostname,vendor,os_guess,ttl,open_ports
192.168.1.1,aa:bb:cc:dd:ee:ff,router.local,TP-Link,Linux/Android/macOS,64,80/tcp (http); 443/tcp (https)
```

### Example JSON Output:
```json
[
  {
    "ip": "192.168.1.1",
    "mac": "aa:bb:cc:dd:ee:ff",
    "hostname": "router.local",
    "vendor": "TP-Link",
    "os_guess": "Linux/Android/macOS",
    "ttl": 64,
    "open_ports": ["80/tcp (http)", "443/tcp (https)"]
  }
]
```

## Technical Notes

- **TTL fingerprinting:** The TTL received from an ICMP reply passes through multiple hops so it is always ≤ the original TTL. Inference rules:
  - TTL ≤ 64 → Linux / Android / macOS (default TTL: 64)
  - TTL ≤ 128 → Windows (default TTL: 128)
  - TTL ≤ 255 → Cisco / Network Device (default TTL: 255)
- **Port scan** uses `-sT` (TCP connect scan) instead of `-sS` (SYN scan) to avoid needing extra raw socket privileges.
- **ARP scan** uses Scapy's `srp()` with Ethernet broadcast for maximum LAN coverage.
- **MAC lookup** uses `mac-vendor-lookup` library with IEEE OUI database.

## Verified Results

✅ Successfully scanned local LAN, correctly identified:
- Router devices (TP-Link, Asus)
- Windows laptops with correct TTL fingerprinting
- Linux servers and Android phones
- Network switches and smart devices

## Troubleshooting

```bash
# If you see "Permission denied" for raw socket
sudo venv/bin/python src/main.py <target>

# If nmap is not installed
sudo pacman -S nmap
```

## References

- [Scapy Documentation](https://scapy.net/)
- [Nmap Reference Guide](https://nmap.org/book/man.html)
- [IEEE MAC Vendor Lookup](https://mac-vendor-lookup.readthedocs.io/)
- [TTL Values by Operating System](https://en.wikipedia.org/wiki/Default_TTL_values)

<p align="right">

⬆️ <a href="#language">Back to Language Selection</a>

</p>

---

<a id="tieng-viet"></a>

# 🇻🇳 Tiếng Việt

# 🔍 02 - Network Scanner — Khám phá tài sản mạng

## Mô tả

Quét mạng LAN, phát hiện thiết bị online, nhận diện hệ điều hành và scan port mở. Công cụ này thực hiện khám phá tài sản mạng toàn diện sử dụng ARP scan, OS fingerprinting dựa trên TTL, và port scan bằng Nmap.

## Tính năng

- [x] ARP scan phát hiện thiết bị online trong LAN
- [x] Resolve hostname qua reverse DNS
- [x] Tra cứu MAC vendor (cơ sở dữ liệu IEEE OUI)
- [x] OS fingerprint qua TTL (Linux/Windows/Network device)
- [x] Port scan (tùy chọn) dùng Nmap TCP connect scan
- [x] Output dạng bảng đẹp với format màu sắc
- [x] Xuất báo cáo CSV và JSON có timestamp
- [x] Chỉ báo tiến trình trong quá trình quét

## Kỹ năng thực hành

`Python` `Scapy` `Nmap` `ARP` `Socket` `TTL Fingerprinting` `Asset Discovery`

## Cài đặt

```bash
# Cài đặt công cụ hệ thống (Arch/Garuda)
sudo pacman -S nmap tshark wireshark-qt

# Cài đặt thư viện Python
pip install scapy python-nmap rich
```

## Cách chạy

```bash
# Activate venv trước
source venv/bin/activate

# Chỉ ARP scan + OS fingerprint (nhanh)
sudo venv/bin/python src/main.py 192.168.1.0/24

# Kèm port scan (chậm hơn, đầy đủ)
sudo venv/bin/python src/main.py 192.168.1.0/24 --ports

# Toàn bộ dải port (chậm nhưng toàn diện)
sudo venv/bin/python src/main.py 192.168.1.0/24 --ports --port-range 1-65535
```

### Các đối số dòng lệnh

| Đối số | Kiểu | Mặc định | Mô tả |
|--------|------|----------|-------|
| `target` | positional | bắt buộc | Dải IP cần quét, vd: `192.168.1.0/24` |
| `--ports` | flag | false | Bật port scanning (yêu cầu Nmap) |
| `--port-range` | string | `1-1000` | Dải port cần quét, vd: `1-65535` |

### Quyền hạn

⚠️ Công cụ này **yêu cầu `sudo`** vì tạo raw socket cho gói ARP và ICMP.

## Cấu trúc dự án

```
02-network-scanner/
├── src/
│   ├── main.py                  # Entry point với CLI
│   └── scanner/
│       ├── arp.py               # ARP scan phát hiện thiết bị
│       ├── fingerprint.py        # OS detection qua TTL
│       ├── ports.py              # Port scan qua Nmap
│       ├── lookup.py             # DNS resolution + MAC vendor
│       ├── display.py            # Output dạng bảng rich
│       └── exporter.py           # Xuất báo cáo CSV/JSON
├── docs/
│   └── screenshots/              # Ảnh chụp kết quả quét
└── README.md
```

## Output

Kết quả được lưu tại `output/reports/` dưới dạng CSV và JSON, có timestamp.

### Ví dụ CSV:
```
ip,mac,hostname,vendor,os_guess,ttl,open_ports
192.168.1.1,aa:bb:cc:dd:ee:ff,router.local,TP-Link,Linux/Android/macOS,64,80/tcp (http); 443/tcp (https)
```

### Ví dụ JSON:
```json
[
  {
    "ip": "192.168.1.1",
    "mac": "aa:bb:cc:dd:ee:ff",
    "hostname": "router.local",
    "vendor": "TP-Link",
    "os_guess": "Linux/Android/macOS",
    "ttl": 64,
    "open_ports": ["80/tcp (http)", "443/tcp (https)"]
  }
]
```

## Ghi chú kỹ thuật

- **TTL fingerprinting:** TTL nhận được từ ICMP reply đi qua nhiều hop nên luôn ≤ TTL gốc. Quy tắc suy luận:
  - TTL ≤ 64 → Linux / Android / macOS (TTL mặc định: 64)
  - TTL ≤ 128 → Windows (TTL mặc định: 128)
  - TTL ≤ 255 → Cisco / Network Device (TTL mặc định: 255)
- **Port scan** dùng `-sT` (TCP connect scan) thay vì `-sS` (SYN scan) để không cần thêm quyền raw socket phức tạp.
- **ARP scan** sử dụng `srp()` của Scapy với Ethernet broadcast để phủ toàn bộ LAN.
- **Tra cứu MAC** dùng thư viện `mac-vendor-lookup` với cơ sở dữ liệu IEEE OUI.

## Kết quả đã kiểm chứng

✅ Đã quét thành công LAN thực tế, xác định chính xác:
- Router (TP-Link, Asus)
- Laptop Windows với fingerprinting TTL đúng
- Server Linux và điện thoại Android
- Switch và thiết bị thông minh

## Xử lý sự cố

```bash
# Nếu gặp lỗi "Permission denied" cho raw socket
sudo venv/bin/python src/main.py 192.168.1.0/24

# Nếu chưa cài nmap
sudo pacman -S nmap
```

## Tham khảo

- [Tài liệu Scapy](https://scapy.net/)
- [Hướng dẫn Nmap](https://nmap.org/book/man.html)
- [Tra cứu MAC Vendor IEEE](https://mac-vendor-lookup.readthedocs.io/)
- [Giá trị TTL theo Hệ điều hành](https://en.wikipedia.org/wiki/Default_TTL_values)

<p align="right">

⬆️ <a href="#language">Quay lại chọn ngôn ngữ</a>

</p>