from scapy.all import *
from scapy.layers.dns import *


def dns_filter(pack):
    if (DNS in pack) and (DNSQR in pack):
        return (pack[DNS].opcode == 0) and (pack[DNSQR].qtype == 1)


def print_qname(pack):
    print(pack[DNSQR].qname.decode())


def main():
    p = sniff(count=6, lfilter=dns_filter, prn=print_qname)


if __name__ == '__main__':
    main()
