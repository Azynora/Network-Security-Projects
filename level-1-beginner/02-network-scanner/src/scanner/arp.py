"""ARP scan phát hiện thiết bị online trong LAN"""

from scapy.all import ARP, Ether, srp
from rich.console import Console

from scanner.lookup import get_hostname, get_vendor
from scanner.fingerprint import guess_os_by_ttl

console = Console()


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
