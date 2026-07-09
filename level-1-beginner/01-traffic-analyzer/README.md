k# 📡 01 - Traffic Analyzer

## Mô tả
Phân tích file `.pcap`, thống kê traffic và phát hiện các dấu hiệu tấn công.

## Tính năng
- [x] Parse file .pcap bằng Scapy
- [x] Thống kê: Top talkers, Top protocols, Top ports
- [x] Phát hiện: SYN flood
- [x] Phát hiện: Port scan
- [x] Phát hiện: Ping sweep
- [x] Output dạng bảng đẹp (rich)

## Kỹ năng
`Python` `Scapy` `TCP/IP` `Wireshark` `tcpdump`

## Cách chạy

```bash
source venv/bin/activate

# Phân tích cơ bản
venv/bin/python src/main.py samples/my_traffic.pcap

# Tùy chỉnh ngưỡng phát hiện
venv/bin/python src/main.py samples/attack_test.pcap \
    --syn-threshold 20 \
    --port-threshold 15 \
    --ping-threshold 10
```

## Cách tạo file pcap để test

```bash
# Capture traffic thật
sudo tcpdump -i <interface> -w samples/my_traffic.pcap -c 500

# Giả lập SYN flood để test detection (chỉ target vào IP mình sở hữu)
sudo nping --tcp -p 80 --flags SYN -c 200 --rate 100 <target_ip>
```

## Kết quả đã kiểm chứng
Đã test thành công với traffic thật: phát hiện đúng SYN flood giả lập bằng `nping`,
baseline traffic bình thường không có false positive.

## Ghi chú kỹ thuật
- SYN flood: đếm số gói TCP chỉ có flag SYN (không kèm ACK) từ 1 nguồn IP.
- Port scan: đếm số port đích khác nhau mà 1 cặp (source, destination) đã truy cập.
- Ping sweep: đếm số host khác nhau mà 1 nguồn IP gửi ICMP Echo Request tới.
- Cần kiểm tra `IP in pkt` trước khi truy cập `pkt[IP]` vì traffic có thể là IPv6
  (không có layer IP/IPv4).
