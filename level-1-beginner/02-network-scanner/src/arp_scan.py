#!/usr/bin/env python3
"""
Network Scanner & Asset Discovery
- ARP scan phát hiện thiết bị online trong LAN
- Hostname resolution
- MAC vendor lookup
- OS fingerprint qua TTL
- Port scan (tùy chọn, dùng nmap)
- Xuất báo cáo CSV/JSON

Cần chạy với sudo vì cần raw socket
"""

from scapy.all import ARP, Ether, IP, ICMP, srp, sr1
from mac_vendor_lookup import MacLookup
from rich.console import Console
from rich.table import Table
import nmap
import socket
import csv
import json
import argparse
from datetime import datetime
import os

console = Console()
mac_lookup = MacLookup()


def get_hostname(ip):
    try:
        socket.setdefaulttimeout(1)
        hostname = socket.gethostbyaddr(ip)[0]
        return hostname
    except (socket.herror, socket.timeout, OSError):
        return "N/A"


def get_vendor(mac):
    try:
        return mac_lookup.lookup(mac)
    except Exception:
        return "Unknown"


def guess_os_by_ttl(ip):
    """
    Gửi ICMP ping, đọc TTL trong response để đoán OS
    TTL gốc thường là: 64 (Linux/macOS/Android), 128 (Windows), 255 (Cisco/Network device)
    Do đi qua nhiều hop nên TTL nhận được sẽ <= TTL gốc, cần làm tròn lên mốc gần nhất
    """
    try:
        pkt = IP(dst=ip) / ICMP()
        reply = sr1(pkt, timeout=1, verbose=False)

        if reply is None:
            return "N/A", None

        ttl = reply.ttl

        if ttl <= 64:
            os_guess = "Linux / Android / macOS"
        elif ttl <= 128:
            os_guess = "Windows"
        elif ttl <= 255:
            os_guess = "Cisco / Network Device"
        else:
            os_guess = "Unknown"

        return os_guess, ttl

    except Exception:
        return "N/A", None


def arp_scan(target_ip_range):
    console.print(f"[bold cyan][*] Đang quét ARP dải mạng: {target_ip_range}[/bold cyan]")

    arp_request = ARP(pdst=target_ip_range)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request

    answered_list = srp(arp_request_broadcast, timeout=2, verbose=False)[0]

    devices = []
    with console.status("[bold green]Đang tra cứu hostname, vendor & OS fingerprint...") as status:
        for sent, received in answered_list:
            ip = received.psrc
            mac = received.hwsrc
            hostname = get_hostname(ip)
            vendor = get_vendor(mac)
            os_guess, ttl = guess_os_by_ttl(ip)

            devices.append({
                "ip": ip,
                "mac": mac,
                "hostname": hostname,
                "vendor": vendor,
                "os_guess": os_guess,
                "ttl": ttl,
                "open_ports": []
            })

    return devices


def port_scan(devices, port_range="1-1000"):
    scanner = nmap.PortScanner()

    console.print(f"\n[bold cyan][*] Đang quét port ({port_range}) cho {len(devices)} thiết bị...[/bold cyan]")
    console.print("[dim]   (Có thể mất 30s - vài phút tùy số lượng thiết bị)[/dim]\n")

    for device in devices:
        ip = device["ip"]
        with console.status(f"[bold yellow]Đang quét {ip}...[/bold yellow]"):
            try:
                scanner.scan(ip, port_range, arguments="-sT -T4")

                if ip in scanner.all_hosts():
                    for proto in scanner[ip].all_protocols():
                        ports = scanner[ip][proto].keys()
                        for port in ports:
                            state = scanner[ip][proto][port]["state"]
                            if state == "open":
                                service = scanner[ip][proto][port].get("name", "unknown")
                                device["open_ports"].append(f"{port}/{proto} ({service})")
            except Exception as e:
                console.print(f"[red]Lỗi quét {ip}: {e}[/red]")

    return devices


def print_result(devices, show_ports=False):
    table = Table(title="🛡️  Kết quả quét mạng LAN", show_lines=True)
    table.add_column("IP Address", style="cyan", no_wrap=True)
    table.add_column("MAC Address", style="magenta")
    table.add_column("Hostname", style="green")
    table.add_column("Vendor", style="yellow")
    table.add_column("OS Guess (TTL)", style="blue")

    if show_ports:
        table.add_column("Open Ports", style="red")

    for d in devices:
        ttl_display = f"{d['os_guess']} (TTL={d['ttl']})" if d["ttl"] else d["os_guess"]
        row = [d["ip"], d["mac"], d["hostname"], d["vendor"], ttl_display]
        if show_ports:
            ports_str = "\n".join(d["open_ports"]) if d["open_ports"] else "-"
            row.append(ports_str)
        table.add_row(*row)

    console.print(table)
    console.print(f"\n[bold]Tổng số thiết bị online: {len(devices)}[/bold]\n")


def export_csv(devices, output_dir):
    filename = f"scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ip", "mac", "hostname", "vendor", "os_guess", "ttl", "open_ports"])
        for d in devices:
            ports_str = "; ".join(d["open_ports"])
            writer.writerow([d["ip"], d["mac"], d["hostname"], d["vendor"], d["os_guess"], d["ttl"], ports_str])

    console.print(f"[green]✅ Đã xuất CSV: {filepath}[/green]")


def export_json(devices, output_dir):
    filename = f"scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w") as f:
        json.dump(devices, f, indent=2, ensure_ascii=False)

    console.print(f"[green]✅ Đã xuất JSON: {filepath}[/green]")


if __name__ == "__main__":
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
