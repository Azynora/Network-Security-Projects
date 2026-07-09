"""Đọc file .pcap"""

from scapy.all import rdpcap
from rich.console import Console
import sys

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
