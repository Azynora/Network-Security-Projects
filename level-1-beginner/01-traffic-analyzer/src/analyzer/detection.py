"""Phát hiện tấn công: SYN flood, port scan, ping sweep"""

from scapy.all import IP, TCP, ICMP
from collections import Counter


def detect_syn_flood(packets, threshold=50):
    syn_counter = Counter()
    for pkt in packets:
        if TCP in pkt and IP in pkt:
            flags = pkt[TCP].flags
            if flags == "S":
                syn_counter[pkt[IP].src] += 1
    return {ip: count for ip, count in syn_counter.items() if count >= threshold}


def detect_port_scan(packets, port_threshold=15):
    scan_map = {}
    for pkt in packets:
        if TCP in pkt and IP in pkt:
            src = pkt[IP].src
            dst = pkt[IP].dst
            dport = pkt[TCP].dport
            key = (src, dst)
            if key not in scan_map:
                scan_map[key] = set()
            scan_map[key].add(dport)

    suspects = []
    for (src, dst), ports in scan_map.items():
        if len(ports) >= port_threshold:
            suspects.append({"src": src, "dst": dst, "unique_ports": len(ports)})
    return suspects


def detect_ping_sweep(packets, host_threshold=10):
    ping_map = {}
    for pkt in packets:
        if ICMP in pkt and IP in pkt:
            if pkt[ICMP].type == 8:
                src = pkt[IP].src
                dst = pkt[IP].dst
                if src not in ping_map:
                    ping_map[src] = set()
                ping_map[src].add(dst)
    return {src: len(hosts) for src, hosts in ping_map.items() if len(hosts) >= host_threshold}
