"""Port scan dùng nmap"""

import nmap
from rich.console import Console

console = Console()


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
