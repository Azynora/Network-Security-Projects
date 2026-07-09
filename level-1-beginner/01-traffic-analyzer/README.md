# 📡 01 - Traffic Analyzer

## Description / Mô tả

**EN:** Analyze `.pcap` files, generate traffic statistics, and detect attack signatures.

**VI:** Phân tích file `.pcap`, thống kê traffic và phát hiện các dấu hiệu tấn công.

## Features / Tính năng
- [x] Parse .pcap files with Scapy / Parse file .pcap bằng Scapy
- [x] Statistics: Top talkers, Top protocols, Top ports / Thống kê: Top talkers, Top protocols, Top ports
- [x] Detection: SYN flood / Phát hiện: SYN flood
- [x] Detection: Port scan / Phát hiện: Port scan
- [x] Detection: Ping sweep / Phát hiện: Ping sweep
- [x] Rich table output / Output dạng bảng đẹp (rich)

## Skills / Kỹ năng
`Python` `Scapy` `TCP/IP` `Wireshark` `tcpdump`

## Usage / Cách chạy

```bash
source venv/bin/activate

# Basic analysis / Phân tích cơ bản
venv/bin/python src/main.py samples/my_traffic.pcap

# Custom detection thresholds / Tùy chỉnh ngưỡng phát hiện
venv/bin/python src/main.py samples/attack_test.pcap \
    --syn-threshold 20 \
    --port-threshold 15 \
    --ping-threshold 10
```

## Generating test pcap files / Cách tạo file pcap để test

```bash
# Capture live traffic / Capture traffic thật
sudo tcpdump -i <interface> -w samples/my_traffic.pcap -c 500

# Simulate SYN flood (target your own IP only!) / Giả lập SYN flood để test (chỉ target vào IP mình sở hữu)
sudo nping --tcp -p 80 --flags SYN -c 200 --rate 100 <target_ip>
```

## Verified Results / Kết quả đã kiểm chứng

**EN:** Successfully tested with real traffic: correctly detected simulated SYN flood via `nping`, normal baseline traffic produced no false positives.

**VI:** Đã test thành công với traffic thật: phát hiện đúng SYN flood giả lập bằng `nping`, baseline traffic bình thường không có false positive.

## Technical Notes / Ghi chú kỹ thuật

**EN:**
- SYN flood: counts TCP packets with only the SYN flag (no ACK) from a single source IP.
- Port scan: counts distinct destination ports accessed by one (source, destination) pair.
- Ping sweep: counts distinct hosts to which one source IP sends ICMP Echo Requests.
- Always check `IP in pkt` before accessing `pkt[IP]` — traffic may be IPv6 (no IP/IPv4 layer).

**VI:**
- SYN flood: đếm số gói TCP chỉ có flag SYN (không kèm ACK) từ 1 nguồn IP.
- Port scan: đếm số port đích khác nhau mà 1 cặp (source, destination) đã truy cập.
- Ping sweep: đếm số host khác nhau mà 1 nguồn IP gửi ICMP Echo Request tới.
- Cần kiểm tra `IP in pkt` trước khi truy cập `pkt[IP]` vì traffic có thể là IPv6 (không có layer IP/IPv4).
