<a id="language"></a>

<div align="right">

## 🌐 Language

🇺🇸 [English](#english)
|
🇻🇳 [Tiếng Việt](#tieng-viet)

</div>

---

<a id="english"></a>

# 🇺🇸 English

# 🔍 02 - Network Scanner — Asset Discovery

## Description

Scan LAN networks, discover online devices, detect operating systems, and scan open ports.

## Features
- [x] ARP scan to discover online LAN devices
- [x] Hostname resolution via reverse DNS
- [x] MAC vendor lookup
- [x] OS fingerprinting via TTL (Linux/Windows/Network device)
- [x] Port scan (optional) using Nmap
- [x] CSV and JSON report export

## Skills
`Python` `Scapy` `Nmap` `ARP` `Socket` `TTL Fingerprinting`

## Usage

```bash
# Activate venv first
source venv/bin/activate

# ARP scan + OS fingerprint only (fast)
sudo venv/bin/python src/main.py 192.168.1.0/24

# With port scan (slower, complete)
sudo venv/bin/python src/main.py 192.168.1.0/24 --ports

# Custom port range
sudo venv/bin/python src/main.py 192.168.1.0/24 --ports --port-range 1-65535
```

## Output

Results are saved to `output/reports/` as CSV and JSON with timestamps.

## Technical Notes

- TTL fingerprinting: the TTL received from an ICMP reply passes through multiple hops so it is always ≤ the original TTL. Inference rules: TTL ≤ 64 → Linux/Android/macOS, TTL ≤ 128 → Windows, TTL ≤ 255 → Cisco/Network device.
- Port scan uses `-sT` (TCP connect scan) instead of `-sS` (SYN scan) to avoid needing extra raw socket privileges.

<p align="right">

⬆️ <a href="#language">Back to Language Selection</a>

</p>

---

<a id="tieng-viet"></a>

# 🇻🇳 Tiếng Việt

# 🔍 02 - Network Scanner — Khám phá tài sản mạng

## Mô tả

Quét mạng LAN, phát hiện thiết bị online, nhận diện OS và scan port mở.

## Tính năng
- [x] ARP scan phát hiện thiết bị online trong LAN
- [x] Resolve hostname qua reverse DNS
- [x] Tra cứu MAC vendor
- [x] OS fingerprint qua TTL (Linux/Windows/Network device)
- [x] Port scan (tùy chọn) dùng nmap
- [x] Xuất báo cáo CSV và JSON

## Kỹ năng
`Python` `Scapy` `Nmap` `ARP` `Socket` `TTL Fingerprinting`

## Cách chạy

```bash
# Activate venv trước
source venv/bin/activate

# Chỉ ARP scan + OS fingerprint (nhanh)
sudo venv/bin/python src/main.py 192.168.1.0/24

# Kèm port scan (chậm hơn, đầy đủ)
sudo venv/bin/python src/main.py 192.168.1.0/24 --ports

# Tùy chỉnh dải port
sudo venv/bin/python src/main.py 192.168.1.0/24 --ports --port-range 1-65535
```

## Output

Kết quả được lưu tại `output/reports/` dưới dạng CSV và JSON, có timestamp.

## Ghi chú kỹ thuật

- TTL fingerprinting: TTL nhận được từ ICMP reply đi qua nhiều hop nên luôn ≤ TTL gốc. Quy tắc suy luận: TTL ≤ 64 → Linux/Android/macOS, TTL ≤ 128 → Windows, TTL ≤ 255 → Cisco/Network device.
- Port scan dùng `-sT` (TCP connect scan) thay vì `-sS` (SYN scan) để không cần thêm quyền raw socket phức tạp.

<p align="right">

⬆️ <a href="#language">Quay lại chọn ngôn ngữ</a>

</p>
