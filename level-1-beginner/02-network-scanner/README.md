# 🔍 02 - Network Scanner — Asset Discovery

## Description / Mô tả

**EN:** Scan LAN networks, discover online devices, detect operating systems, and scan open ports.

**VI:** Quét mạng LAN, phát hiện thiết bị online, nhận diện OS và scan port mở.

## Features / Tính năng
- [x] ARP scan to discover online LAN devices / ARP scan phát hiện thiết bị online trong LAN
- [x] Hostname resolution via reverse DNS / Resolve hostname qua reverse DNS
- [x] MAC vendor lookup / Tra cứu MAC vendor
- [x] OS fingerprinting via TTL (Linux/Windows/Network device) / OS fingerprint qua TTL
- [x] Port scan (optional) using Nmap / Port scan (tùy chọn) dùng nmap
- [x] CSV and JSON report export / Xuất báo cáo CSV và JSON

## Skills / Kỹ năng
`Python` `Scapy` `Nmap` `ARP` `Socket` `TTL Fingerprinting`

## Usage / Cách chạy

```bash
# Activate venv first / Activate venv trước
source venv/bin/activate

# ARP scan + OS fingerprint only (fast) / Chỉ ARP scan + OS fingerprint (nhanh)
sudo venv/bin/python src/main.py 192.168.1.0/24

# With port scan (slower, complete) / Kèm port scan (chậm hơn, đầy đủ)
sudo venv/bin/python src/main.py 192.168.1.0/24 --ports

# Custom port range / Tùy chỉnh dải port
sudo venv/bin/python src/main.py 192.168.1.0/24 --ports --port-range 1-65535
```

## Output

**EN:** Results are saved to `output/reports/` as CSV and JSON with timestamps.

**VI:** Kết quả được lưu tại `output/reports/` dưới dạng CSV và JSON, có timestamp.

## Technical Notes / Ghi chú kỹ thuật

**EN:**
- TTL fingerprinting: the TTL received from an ICMP reply passes through multiple hops so it is always ≤ the original TTL. Inference rules: TTL ≤ 64 → Linux/Android/macOS, TTL ≤ 128 → Windows, TTL ≤ 255 → Cisco/Network device.
- Port scan uses `-sT` (TCP connect scan) instead of `-sS` (SYN scan) to avoid needing extra raw socket privileges.

**VI:**
- TTL fingerprinting: TTL nhận được từ ICMP reply đi qua nhiều hop nên luôn ≤ TTL gốc. Quy tắc suy luận: TTL ≤ 64 → Linux/Android/macOS, TTL ≤ 128 → Windows, TTL ≤ 255 → Cisco/Network device.
- Port scan dùng `-sT` (TCP connect scan) thay vì `-sS` (SYN scan) để không cần thêm quyền raw socket phức tạp.
