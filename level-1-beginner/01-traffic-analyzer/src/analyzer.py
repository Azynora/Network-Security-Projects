#!/usr/bin/env python3
"""
Traffic Analyzer - Phân tích file .pcap
- Thống kê: Top talkers, Top protocols, Top ports
- Phát hiện: SYN flood, Ping sweep, Port scan
"""

from scapy.all import rdpcap, IP, TCP, UDP, ICMP
from collections import Counter
from rich.console import Console
from rich.table import Table
import argparse
import sys
import os

console = Console()


def load_pcap(filepath):
    console.print(f"[bold cyan][*] Đang đọc file: {filepath}[/bold cyan]")
    try:
        packets = rdpcap(filepath)
        console.print(f"[green]✅ Đã đọc {len(packets)} packets[/green]\n")
        return packets
    except Exception as e:
        console.print(f"[red]Lỗi đọc file: {e}[/red]")
        sys.exit(1)


def analyze_top_talkers(packets, top_n=10):
    ip_counter = Counter()

    for pkt in packets:
        if IP in pkt:
            ip_counter[pkt[IP].src] += 1
            ip_counter[pkt[IP].dst] += 1

    return ip_counter.most_common(top_n)


def analyze_protocols(packets):
    proto_counter = Counter()

    for pkt in packets:
        if TCP in pkt:
            proto_counter["TCP"] += 1
        elif UDP in pkt:
            proto_counter["UDP"] += 1
        elif ICMP in pkt:
            proto_counter["ICMP"] += 1
        else:
            proto_counter["Other"] += 1

    return proto_counter


def analyze_top_ports(packets, top_n=10):
    port_counter = Counter()

    for pkt in packets:
        if TCP in pkt:
            port_counter[f"{pkt[TCP].dport}/tcp"] += 1
        elif UDP in pkt:
            port_counter[f"{pkt[UDP].dport}/udp"] += 1

    return port_counter.most_common(top_n)


def print_top_talkers(talkers):
    table = Table(title="📊 Top Talkers (IP hoạt động nhiều nhất)")
    table.add_column("IP Address", style="cyan")
    table.add_column("Số Packets", style="magenta", justify="right")

    for ip, count in talkers:
        table.add_row(ip, str(count))

    console.print(table)


def print_protocols(proto_counter):
    table = Table(title="📊 Phân bố Protocol")
    table.add_column("Protocol", style="green")
    table.add_column("Số Packets", style="magenta", justify="right")

    for proto, count in proto_counter.most_common():
        table.add_row(proto, str(count))

    console.print(table)


def print_top_ports(ports):
    table = Table(title="📊 Top Ports được truy cập")
    table.add_column("Port", style="yellow")
    table.add_column("Số Packets", style="magenta", justify="right")

    for port, count in ports:
        table.add_row(port, str(count))

    console.print(table)

def detect_syn_flood(packets, threshold=50):
    """
    Phát hiện SYN flood: 1 nguồn IP gửi quá nhiều SYN packet (không có ACK phản hồi)
    tới nhiều port/host khác nhau trong thời gian ngắn
    """
    syn_counter = Counter()

    for pkt in packets:
        if TCP in pkt and IP in pkt:
            flags = pkt[TCP].flags
            # flags == 'S' nghĩa là chỉ có SYN flag, không có ACK -> nghi vấn
            if flags == "S":
                syn_counter[pkt[IP].src] += 1

    suspects = {ip: count for ip, count in syn_counter.items() if count >= threshold}
    return suspects


def detect_port_scan(packets, port_threshold=15):
    """
    Phát hiện port scan: 1 nguồn IP quét nhiều port khác nhau trên cùng 1 đích
    """
    # {(src_ip, dst_ip): set(các port đã quét)}
    scan_map = {}

    for pkt in packets:
        if TCP in pkt and IP in pkt:
            src = pkt[IP].src
            dst = pkt[IP].dst
            dport = pkt[TCP].dport
            key = (src, dst)

            if key not in scan_map:
                scan_map[key] = set()
            scan_map[key].add(dport)

    suspects = []
    for (src, dst), ports in scan_map.items():
        if len(ports) >= port_threshold:
            suspects.append({"src": src, "dst": dst, "unique_ports": len(ports)})

    return suspects


def detect_ping_sweep(packets, host_threshold=10):
    """
    Phát hiện ping sweep: 1 nguồn IP gửi ICMP echo request tới nhiều host khác nhau
    """
    ping_map = {}

    for pkt in packets:
        if ICMP in pkt and IP in pkt:
            if pkt[ICMP].type == 8:  # Echo Request
                src = pkt[IP].src
                dst = pkt[IP].dst

                if src not in ping_map:
                    ping_map[src] = set()
                ping_map[src].add(dst)

    suspects = {src: len(hosts) for src, hosts in ping_map.items() if len(hosts) >= host_threshold}
    return suspects


def print_detections(syn_suspects, portscan_suspects, pingsweep_suspects):
    console.print("\n[bold red]🚨 KẾT QUẢ PHÁT HIỆN BẤT THƯỜNG[/bold red]\n")

    # SYN Flood
    if syn_suspects:
        table = Table(title="⚠️  Nghi vấn SYN Flood", border_style="red")
        table.add_column("Source IP", style="red")
        table.add_column("Số lượng SYN packet", style="yellow", justify="right")
        for ip, count in syn_suspects.items():
            table.add_row(ip, str(count))
        console.print(table)
    else:
        console.print("[green]✅ Không phát hiện SYN flood[/green]")

    console.print()

    # Port Scan
    if portscan_suspects:
        table = Table(title="⚠️  Nghi vấn Port Scan", border_style="red")
        table.add_column("Source IP", style="red")
        table.add_column("Target IP", style="cyan")
        table.add_column("Số port khác nhau", style="yellow", justify="right")
        for s in portscan_suspects:
            table.add_row(s["src"], s["dst"], str(s["unique_ports"]))
        console.print(table)
    else:
        console.print("[green]✅ Không phát hiện port scan[/green]")

    console.print()

    # Ping Sweep
    if pingsweep_suspects:
        table = Table(title="⚠️  Nghi vấn Ping Sweep", border_style="red")
        table.add_column("Source IP", style="red")
        table.add_column("Số host bị ping", style="yellow", justify="right")
        for ip, count in pingsweep_suspects.items():
            table.add_row(ip, str(count))
        console.print(table)
    else:
        console.print("[green]✅ Không phát hiện ping sweep[/green]")

    console.print()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Traffic Analyzer - Phân tích file .pcap")
    parser.add_argument("pcap_file", help="Đường dẫn tới file .pcap")
    parser.add_argument("--syn-threshold", type=int, default=50, help="Ngưỡng SYN packet để cảnh báo flood")
    parser.add_argument("--port-threshold", type=int, default=15, help="Ngưỡng số port khác nhau để cảnh báo port scan")
    parser.add_argument("--ping-threshold", type=int, default=10, help="Ngưỡng số host bị ping để cảnh báo ping sweep")
    args = parser.parse_args()

    if not os.path.exists(args.pcap_file):
        console.print(f"[red]File không tồn tại: {args.pcap_file}[/red]")
        sys.exit(1)

    packets = load_pcap(args.pcap_file)

    talkers = analyze_top_talkers(packets)
    print_top_talkers(talkers)
    console.print()

    protocols = analyze_protocols(packets)
    print_protocols(protocols)
    console.print()

    ports = analyze_top_ports(packets)
    print_top_ports(ports)
    console.print()

    syn_suspects = detect_syn_flood(packets, args.syn_threshold)
    portscan_suspects = detect_port_scan(packets, args.port_threshold)
    pingsweep_suspects = detect_ping_sweep(packets, args.ping_threshold)

    print_detections(syn_suspects, portscan_suspects, pingsweep_suspects)
