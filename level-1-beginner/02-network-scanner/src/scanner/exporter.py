"""Xuất báo cáo ra CSV và JSON"""

import csv
import json
import os
from datetime import datetime
from rich.console import Console

console = Console()


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
