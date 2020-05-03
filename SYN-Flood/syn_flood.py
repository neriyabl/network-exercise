from scapy.layers.inet import TCP, IP
from scapy.utils import rdpcap


def main():
    pcap_file = rdpcap("SynFloodSample.pcap")
    # create set with all ip's from packets with sync flag
    black_set = {p[IP].src for p in pcap_file if p[TCP].flags == 'S'}
    # remove all the ip's that answered with ack
    black_set.difference_update({p[IP].src for p in pcap_file if 'A' in p[TCP].flags})
    with open('blacklist ips.txt', 'w') as ips_file:
        ips_file.write('\n'.join(sorted(black_set)))


if __name__ == '__main__':
    main()
