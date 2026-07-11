<a id="language"></a>

<div align="right">

## 🌐 Language

🇺🇸 [English](#english) | 🇻🇳 [Tiếng Việt](#tieng-viet)

</div>

---

<a id="english"></a>

# 🇺🇸 English

# 📡 01 - Traffic Analyzer

## Description

Analyze `.pcap` files, generate traffic statistics, and detect attack signatures. This tool parses network capture files and provides comprehensive analysis including top talkers, protocol distribution, and attack detection.

## Features

- [x] Parse .pcap files with Scapy
- [x] Statistics: Top talkers, Top protocols, Top ports
- [x] Detection: SYN flood (TCP flag-based)
- [x] Detection: Port scan (distinct port access counting)
- [x] Detection: Ping sweep (ICMP Echo Request counting)
- [x] Rich table output with colorized formatting
- [x] Configurable detection thresholds
- [x] IPv4/IPv6 dual-stack support

## Skills Practiced

`Python` `Scapy` `TCP/IP` `Wireshark` `tcpdump` `Network Forensics`

## Installation

```bash
# Clone and setup virtual environment
cd level-1-beginner/01-traffic-analyzer
python -m venv ../../venv
source ../../venv/bin/activate
pip install -r requirements.txt

# Or use system Python with dependencies
sudo pip install scapy rich pyshark
```

## Usage

```bash
# Basic analysis
venv/bin/python src/main.py samples/my_traffic.pcap

# Custom detection thresholds
venv/bin/python src/main.py samples/attack_test.pcap \
    --syn-threshold 20 \
    --port-threshold 15 \
    --ping-threshold 10

# Output to file
venv/bin/python src/main.py samples/capture.pcap > results.txt
```

### Command Line Arguments

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `pcap_file` | positional | - | Path to the .pcap file to analyze |
| `--syn-threshold` | int | 50 | Minimum SYN packets to trigger flood alert |
| `--port-threshold` | int | 15 | Minimum unique ports to trigger port scan alert |
| `--ping-threshold` | int | 10 | Minimum hosts pinged to trigger sweep alert |

## Project Structure

```
01-traffic-analyzer/
├── src/
│   ├── main.py              # Entry point with CLI
│   └── analyzer/
│       ├── loader.py        # PCAP file loading with Scapy
│       ├── stats.py         # Traffic statistics calculation
│       ├── detection.py     # Attack detection algorithms
│       └── display.py       # Rich table output formatting
├── samples/
│   ├── my_traffic.pcap      # Sample capture file
│   └── attack_test.pcap     # Test file with attack patterns
├── docs/
│   └── screenshots/         # Analysis result screenshots
└── README.md
```

## Generating Test PCAP Files

```bash
# Capture live traffic
sudo tcpdump -i <interface> -w samples/my_traffic.pcap -c 500

# Simulate SYN flood (target your own IP only!)
sudo nping --tcp -p 80 --flags SYN -c 200 --rate 100 <target_ip>

# Simulate port scan
nmap -sS -p 1-1000 <target_ip>

# Generate ICMP ping sweep
for i in {1..100}; do ping -c 1 -W 1 192.168.1.$i; done
```

## Detection Logic

### SYN Flood Detection
- Counts TCP packets with only the SYN flag (no ACK)
- Threshold-based: alerts when SYN count ≥ threshold
- Identifies potential DoS attack sources

### Port Scan Detection
- Counts distinct destination ports accessed by (source, destination) pairs
- Threshold-based: alerts when unique ports ≥ threshold
- Helps identify reconnaissance activity

### Ping Sweep Detection
- Counts distinct hosts receiving ICMP Echo Requests from a single source
- Threshold-based: alerts when hosts pinged ≥ threshold
- Detects network discovery scans

## Verified Results

✅ **Successfully tested with real traffic**
- Correctly detected simulated SYN flood via `nping`
- No false positives on normal baseline traffic
- Accurate port and protocol statistics

## Technical Notes

- Always check `IP in pkt` before accessing `pkt[IP]` — traffic may be IPv6 (no IPv4 layer)
- Uses `rdpcap()` for efficient batch loading
- Counter objects provide O(n) performance for statistics
- Detection thresholds are configurable for different network sizes

## References

- [Scapy Documentation](https://scapy.net/)
- [Wireshark User Guide](https://www.wireshark.org/docs/)
- [TCP/IP Illustrated, Volume 1](https://www.amazon.com/dp/0201533487)

<p align="right">

⬆️ <a href="#language">Back to Language Selection</a>

</p>

---

<a id="tieng-viet"></a>

# 🇻🇳 Tiếng Việt

# 📡 01 - Traffic Analyzer

## Mô tả

Phân tích file `.pcap`, thống kê traffic và phát hiện các dấu hiệu tấn công. Công cụ này phân tích các file bắt gói mạng và cung cấp thống kê toàn diện bao gồm top talkers, phân bố giao thức và phát hiện tấn công.

## Tính năng

- [x] Parse file .pcap bằng Scapy
- [x] Thống kê: Top talkers, Top protocols, Top ports
- [x] Phát hiện: SYN flood (dựa trên TCP flag)
- [x] Phát hiện: Port scan (đếm số port truy cập khác nhau)
- [x] Phát hiện: Ping sweep (đếm số ICMP Echo Request)
- [x] Output dạng bảng đẹp với format màu sắc
- [x] Ngưỡng phát hiện có thể cấu hình
- [x] Hỗ trợ IPv4/IPv6

## Kỹ năng thực hành

`Python` `Scapy` `TCP/IP` `Wireshark` `tcpdump` `Network Forensics`

## Cài đặt

```bash
# Clone và setup môi trường ảo
cd level-1-beginner/01-traffic-analyzer
python -m venv ../../venv
source ../../venv/bin/activate
pip install -r requirements.txt

# Hoặc dùng Python hệ thống với dependencies
sudo pip install scapy rich pyshark
```

## Cách chạy

```bash
# Phân tích cơ bản
venv/bin/python src/main.py samples/my_traffic.pcap

# Phát hiện với ngưỡng tùy chỉnh
venv/bin/python src/main.py samples/attack_test.pcap \
    --syn-threshold 20 \
    --port-threshold 15 \
    --ping-threshold 10

# Output lưu vào file
venv/bin/python src/main.py samples/capture.pcap > results.txt
```

### Các đối số dòng lệnh

| Đối số | Kiểu | Mặc định | Mô tả |
|--------|------|----------|-------|
| `pcap_file` | positional | - | Đường dẫn đến file .pcap cần phân tích |
| `--syn-threshold` | int | 50 | Số lần SYN tối thiểu để báo cáo flood |
| `--port-threshold` | int | 15 | Số port khác nhau tối thiểu để báo cáo port scan |
| `--ping-threshold` | int | 10 | Số host ping tối thiểu để báo cáo ping sweep |

## Cấu trúc dự án

```
01-traffic-analyzer/
├── src/
│   ├── main.py              # Entry point với CLI
│   └── analyzer/
│       ├── loader.py        # Đọc file .pcap bằng Scapy
│       ├── stats.py         # Tính toán thống kê traffic
│       ├── detection.py     # Thuật toán phát hiện tấn công
│       └── display.py       # Format output bảng rich
├── samples/
│   ├── my_traffic.pcap      # File mẫu bắt gói
│   └── attack_test.pcap     # File test có pattern tấn công
├── docs/
│   └── screenshots/         # Ảnh chụp kết quả phân tích
└── README.md
```

## Tạo file PCAP để test

```bash
# Capture traffic thật
sudo tcpdump -i <interface> -w samples/my_traffic.pcap -c 500

# Giả lập SYN flood (chỉ target vào IP của bạn!)
sudo nping --tcp -p 80 --flags SYN -c 200 --rate 100 <target_ip>

# Giả lập port scan
nmap -sS -p 1-1000 <target_ip>

# Tạo ICMP ping sweep
for i in {1..100}; do ping -c 1 -W 1 192.168.1.$i; done
```

## Logic phát hiện

### SYN Flood Detection
- Đếm các gói TCP chỉ có flag SYN (không có ACK)
- Dựa trên ngưỡng: báo cáo khi số lần SYN ≥ ngưỡng
- Xác định nguồn tấn công DoS

### Port Scan Detection
- Đếm số port đích khác nhau mà (source, destination) truy cập
- Dựa trên ngưỡng: báo cáo khi port khác nhau ≥ ngưỡng
- Phát hiện hoạt động khám phá mạng

### Ping Sweep Detection
- Đếm số host nhận ICMP Echo Request từ 1 nguồn duy nhất
- Dựa trên ngưỡng: báo cáo khi host ping ≥ ngưỡng
- Phát hiện scan khám phá mạng

## Kết quả đã kiểm chứng

✅ **Đã test thành công với traffic thật**
- Phát hiện đúng SYN flood giả lập bằng `nping`
- Không có false positive với traffic cơ sở
- Thống kê port và giao thức chính xác

## Ghi chú kỹ thuật

- Luôn kiểm tra `IP in pkt` trước khi truy cập `pkt[IP]` — traffic có thể là IPv6 (không có layer IPv4)
- Sử dụng `rdpcap()` cho việc load batch hiệu quả
- Các đối tượng Counter cung cấp hiệu suất O(n) cho thống kê
- Các ngưỡng phát hiện có thể cấu hình cho kích thước mạng khác nhau

## Tham khảo

- [Tài liệu Scapy](https://scapy.net/)
- [Hướng dẫn Wireshark](https://www.wireshark.org/docs/)
- [TCP/IP Illustrated, Volume 1](https://www.amazon.com/dp/0201533487)

<p align="right">

⬆️ <a href="#language">Quay lại chọn ngôn ngữ</a>

</p>