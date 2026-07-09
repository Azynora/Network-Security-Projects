"""Hiển thị kết quả dạng bảng"""

from rich.console import Console
from rich.table import Table

console = Console()


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
