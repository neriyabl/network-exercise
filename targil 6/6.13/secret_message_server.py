from scapy.all import *
from scapy.layers.inet import UDP, IP

CLIENT_IP = '10.7.10.37'


def client_filter(pack):
    if UDP in pack:
        return pack[IP].src == CLIENT_IP


def print_pack(pack):
    print(chr(pack[UDP].sport), sep='')


def main():
    while True:
        sniff(count=1, lfilter=client_filter, prn=print_pack)


if __name__ == '__main__':
    main()
