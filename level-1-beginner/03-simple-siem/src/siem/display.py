"""Hiển thị kết quả dạng bảng"""

from rich.console import Console
from rich.table import Table

console = Console()

PRIORITY_MAP = {
    "0": "EMERG", "1": "ALERT", "2": "CRIT", "3": "ERR",
    "4": "WARNING", "5": "NOTICE", "6": "INFO", "7": "DEBUG"
}


def print_logs(logs, limit=30):
    table = Table(title=f"📋 System Logs (hiển thị {min(len(logs), limit)}/{len(logs)})")
    table.add_column("Priority", style="bold")
    table.add_column("Unit/Process", style="cyan")
    table.add_column("PID", style="dim")
    table.add_column("Message", style="white")

    for log in logs[-limit:]:
        priority_label = PRIORITY_MAP.get(log["priority"], "N/A")
        style = "red" if priority_label in ("EMERG", "ALERT", "CRIT", "ERR") else \
                "yellow" if priority_label == "WARNING" else "green"
        table.add_row(
            f"[{style}]{priority_label}[/{style}]",
            log["unit"],
            str(log["pid"]),
            log["message"][:90]
        )

    console.print(table)
    console.print(f"\n[bold]Tổng số log entries: {len(logs)}[/bold]\n")


def print_sudo_brute_force(suspects):
    if not suspects:
        console.print("[green]✅ Không phát hiện dấu hiệu sudo brute-force[/green]\n")
        return

    table = Table(title="⚠️  Nghi vấn Sudo Brute-force", border_style="red")
    table.add_column("User", style="red")
    table.add_column("Số lần nhập sai", style="yellow", justify="right")

    for user, entries in suspects.items():
        table.add_row(user, str(len(entries)))

    console.print(table)
    console.print()


def print_failed_ssh(rows):
    if not rows:
        console.print("[green]✅ Không phát hiện SSH login thất bại[/green]\n")
        return

    table = Table(title="⚠️  SSH Login thất bại", border_style="red")
    table.add_column("PID", style="dim")
    table.add_column("Message", style="white")

    for row in rows[:20]:
        table.add_row(str(row["pid"]), row["message"][:100])

    console.print(table)
    console.print(f"\n[bold]Tổng: {len(rows)} lần thất bại[/bold]\n")
