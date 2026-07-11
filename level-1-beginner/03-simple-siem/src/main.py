#!/usr/bin/env python3
"""
Simple SIEM - Log Collector & Detection
Entry point

Cách dùng:
    python main.py collect --minutes 60 --save
    python main.py detect --sudo-threshold 3
"""

import argparse
from rich.console import Console

from siem.journal_reader import read_journal_logs
from siem.storage import init_db, save_logs
from siem.detection import detect_sudo_brute_force, detect_failed_ssh_login
from siem.display import print_logs, print_sudo_brute_force, print_failed_ssh
from siem.es_indexer import index_logs_to_es, index_alerts_to_es

console = Console()


def cmd_collect(args):
    logs = read_journal_logs(args.minutes, args.priority)
    print_logs(logs, args.limit)

    if args.save:
        init_db()
        save_logs(logs)

def cmd_index(args):
    index_logs_to_es()

def cmd_detect(args):
    console.print("[bold red]🚨 KẾT QUẢ PHÁT HIỆN BẤT THƯỜNG TỪ LOG[/bold red]\n")

    sudo_suspects = detect_sudo_brute_force(args.sudo_threshold)
    print_sudo_brute_force(sudo_suspects)

    ssh_failed = detect_failed_ssh_login()
    print_failed_ssh(ssh_failed)

def cmd_alerts(args):
    """Chạy detection và đẩy kết quả alerts lên Elasticsearch"""
    from siem.detection import detect_sudo_brute_force
    from siem.display import print_sudo_brute_force

    console.print("[bold cyan][*] Đang chạy detection...[/bold cyan]")
    sudo_suspects = detect_sudo_brute_force(args.sudo_threshold)
    print_sudo_brute_force(sudo_suspects)
    index_alerts_to_es(sudo_suspects)

def cmd_pipeline(args):
    """Thu thập -> lưu -> index -> detection -> alert"""

    console.print("[bold cyan]=== SIEM Pipeline ===[/bold cyan]")

    logs = read_journal_logs(args.minutes)

    init_db()
    save_logs(logs)

    index_logs_to_es()

    sudo_suspects = detect_sudo_brute_force(args.sudo_threshold)

    print_sudo_brute_force(sudo_suspects)

    index_alerts_to_es(sudo_suspects)

    console.print("[bold green]Pipeline hoàn thành[/bold green]")

def main():
    parser = argparse.ArgumentParser(description="Simple SIEM - Log Collector & Detection")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Sub-command: collect
    collect_parser = subparsers.add_parser("collect", help="Thu thập log từ journalctl")
    collect_parser.add_argument("--minutes", type=int, default=10, help="Số phút gần đây cần đọc log")
    collect_parser.add_argument("--priority", default=None, help="Lọc theo mức độ: err, warning, info,...")
    collect_parser.add_argument("--limit", type=int, default=30, help="Số dòng log hiển thị tối đa")
    collect_parser.add_argument("--save", action="store_true", help="Lưu log vào SQLite database")
    collect_parser.set_defaults(func=cmd_collect)

    # Sub-command: detect
    detect_parser = subparsers.add_parser("detect", help="Phát hiện hành vi bất thường từ log đã lưu")
    detect_parser.add_argument("--sudo-threshold", type=int, default=3, help="Ngưỡng số lần nhập sai sudo")
    detect_parser.set_defaults(func=cmd_detect)

    # Sub-command: index
    index_parser = subparsers.add_parser("index", help="Đẩy log từ SQLite lên Elasticsearch")
    index_parser.set_defaults(func=cmd_index)

    # Sub-command: alerts
    alerts_parser = subparsers.add_parser("alerts", help="Chạy detection và đẩy alerts lên Elasticsearch")
    alerts_parser.add_argument("--sudo-threshold", type=int, default=3, help="Ngưỡng số lần nhập sai sudo")
    alerts_parser.set_defaults(func=cmd_alerts)
 
    # Sub-command: pipeline
    pipeline_parser = subparsers.add_parser(
        "pipeline",
        help="Thu thập -> lưu -> Elasticsearch -> Detection"
    )

    pipeline_parser.add_argument(
        "--minutes",
        type=int,
        default=10,
        help="Số phút cần thu thập log"
    )

    pipeline_parser.add_argument(
        "--sudo-threshold",
        type=int,
        default=3,
        help="Ngưỡng phát hiện sudo brute-force"
    )

    pipeline_parser.set_defaults(func=cmd_pipeline)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
