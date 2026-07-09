"""Hiển thị kết quả dạng bảng"""

from rich.console import Console
from rich.table import Table

console = Console()


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


def print_detections(syn_suspects, portscan_suspects, pingsweep_suspects):
    console.print("\n[bold red]🚨 KẾT QUẢ PHÁT HIỆN BẤT THƯỜNG[/bold red]\n")

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
