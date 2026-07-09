"""OS fingerprint qua TTL"""

from scapy.all import IP, ICMP, sr1


def guess_os_by_ttl(ip):
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
