#!/usr/bin/env python3
"""
Network Scanner & Asset Discovery
Entry point - cần chạy với sudo vì cần raw socket

Cách dùng:
    sudo venv/bin/python main.py 192.168.1.0/24
    sudo venv/bin/python main.py 192.168.1.0/24 --ports
"""

import argparse
import os

from scanner.arp import arp_scan
from scanner.ports import port_scan
from scanner.display import print_result
from scanner.exporter import export_csv, export_json


def main():
    parser = argparse.ArgumentParser(description="Network Scanner & Asset Discovery")
    parser.add_argument("target", help="Dải IP cần quét, ví dụ: 192.168.1.0/24")
    parser.add_argument("--ports", action="store_true", help="Bật port scan (chậm hơn)")
    parser.add_argument("--port-range", default="1-1000", help="Dải port quét, mặc định 1-1000")
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "..", "output", "reports")
    os.makedirs(output_dir, exist_ok=True)

    devices = arp_scan(args.target)

    if args.ports:
        devices = port_scan(devices, args.port_range)

    print_result(devices, show_ports=args.ports)

    export_csv(devices, output_dir)
    export_json(devices, output_dir)


if __name__ == "__main__":
    main()
