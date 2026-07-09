"""Thống kê traffic: top talkers, protocols, ports"""

from scapy.all import IP, TCP, UDP, ICMP
from collections import Counter


def analyze_top_talkers(packets, top_n=10):
    ip_counter = Counter()
    for pkt in packets:
        if IP in pkt:
            ip_counter[pkt[IP].src] += 1
            ip_counter[pkt[IP].dst] += 1
    return ip_counter.most_common(top_n)


def analyze_protocols(packets):
    proto_counter = Counter()
    for pkt in packets:
        if TCP in pkt:
            proto_counter["TCP"] += 1
        elif UDP in pkt:
            proto_counter["UDP"] += 1
        elif ICMP in pkt:
            proto_counter["ICMP"] += 1
        else:
            proto_counter["Other"] += 1
    return proto_counter


def analyze_top_ports(packets, top_n=10):
    port_counter = Counter()
    for pkt in packets:
        if TCP in pkt:
            port_counter[f"{pkt[TCP].dport}/tcp"] += 1
        elif UDP in pkt:
            port_counter[f"{pkt[UDP].dport}/udp"] += 1
    return port_counter.most_common(top_n)
