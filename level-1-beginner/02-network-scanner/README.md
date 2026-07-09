# 🔍 02 - Network Scannermain & Asset Discovery

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
sudo venv/bin/python src/.py 192.168.1.0/24

# Kèm port scan (chậm hơn, đầy đủ)
sudo venv/bin/python src/arp_scan.py 192.168.1.0/24 --ports

# Tùy chỉnh dải port
sudo venv/bin/python src/arp_scan.py 192.168.1.0/24 --ports --port-range 1-65535
```

## Output
Kết quả được lưu tại `output/reports/` dưới dạng CSV và JSON, có timestamp.

## Ghi chú kỹ thuật
- TTL fingerprinting: TTL nhận được từ ICMP reply đi qua nhiều hop nên luôn <= TTL gốc.
  Quy tắc suy luận: TTL <= 64 → Linux/Android/macOS, TTL <= 128 → Windows, TTL <= 255 → Cisco/Network device.
- Port scan dùng `-sT` (TCP connect scan) thay vì `-sS` (SYN scan) để không cần thêm quyền raw socket phức tạp.
