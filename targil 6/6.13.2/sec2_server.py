from scapy.all import *
from scapy.layers.dns import DNS, DNSQR
from scapy.layers.inet import IP

CLIENT_IP = '10.7.10.37'


def client_filter(pack):
    if (DNS in pack) and (DNSQR in pack):
        return pack[IP].src == CLIENT_IP


def print_pack(pack):
    print(pack[DNS][DNSQR].qname.decode().split('.')[-3][0], end='')


def main():
    while True:
        sniff(count=1000, lfilter=client_filter, prn=print_pack)


if __name__ == '__main__':
    main()
