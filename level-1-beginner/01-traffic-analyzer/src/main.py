#!/usr/bin/env python3
"""
Traffic Analyzer - Phân tích file .pcap
Entry point

Cách dùng:
    python main.py samples/my_traffic.pcap
    python main.py samples/attack_test.pcap --syn-threshold 20
"""

import argparse
import os
import sys

from analyzer.loader import load_pcap
from analyzer.stats import analyze_top_talkers, analyze_protocols, analyze_top_ports
from analyzer.detection import detect_syn_flood, detect_port_scan, detect_ping_sweep
from analyzer.display import print_top_talkers, print_protocols, print_top_ports, print_detections
from rich.console import Console

console = Console()


def main():
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


if __name__ == "__main__":
    main()
