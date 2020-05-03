from scapy.all import *
import time

from scapy.layers.dhcp import DHCP
from scapy.layers.inet import TCP, IP
from scapy.layers.l2 import Ether

MAC = 'ff:ff:ff:ff:ff:ff'


def http_filter(pack):
    return (Ether in pack) and (pack[Ether].dst == MAC)


def print_http(pack):
    print('src: ', pack[Ether].src, '\tdst: ', pack[Ether].dst)


def main():
    sniff(count=2, lfilter=http_filter, prn=print_http)


if __name__ == '__main__':
    main()
