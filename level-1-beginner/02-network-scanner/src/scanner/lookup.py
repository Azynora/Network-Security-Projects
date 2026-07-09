"""Hostname resolution và MAC vendor lookup"""

import socket
from mac_vendor_lookup import MacLookup

mac_lookup = MacLookup()


def get_hostname(ip):
    try:
        socket.setdefaulttimeout(1)
        return socket.gethostbyaddr(ip)[0]
    except (socket.herror, socket.timeout, OSError):
        return "N/A"


def get_vendor(mac):
    try:
        return mac_lookup.lookup(mac)
    except Exception:
        return "Unknown"
