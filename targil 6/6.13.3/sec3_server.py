from scapy.all import *
from scapy.layers.dns import DNS, DNSQR
from scapy.layers.inet import IP

CLIENT_IP = '10.7.10.37'

key = [
    '8?RCYAr>tXSv3LPaTbUyzqF7V9EdH10u',
    'SiGy1tj5MR:Ixrusv2YFN3P;H@J7Vm^K',
    'e2P[TQo9gR7K0_;?usa6NV:wIF5HXrdx',
    'uFZ3OsDXj<^lm@0:kBfc]zUEG;I6`LYW',
    'dwMpEz<krix4gY2s:H_Af57G8FRC@]>?',
    'f^8zPdX>n3:Yo\\7[B02hjs]H@aIQgpyi',
    'Y>e8jgItUbqhkQ@SrB5c7J=Od4RAuCpP'
]

mod = 32
keys_len = 7


def client_filter(pack):
    if (DNS in pack) and (DNSQR in pack):
        return pack[IP].src == CLIENT_IP


def get_mods(key_idx):
    return [key_idx + (i * mod) for i in range(4)]


def print_pack(pack):
    # word = pack[DNS][DNSQR].qname.decode().split('.')[-3]
    word = pack
    for i, char in enumerate(word):
        key_idx = key[i].find(char)
        numbers = get_mods(key_idx)
        if i % 2 == 1:
            numbers = [x * (i + 1) for x in numbers]
        print(numbers)
        # word += key[i][(ascii_val // (i * (i % 2) + 1)) % mod]
    # return word


def main():
    print_pack('RiPkMYe')
    print(chr(65))
    # while True:
    #     sniff(count=1000, lfilter=client_filter, prn=print_pack)


if __name__ == '__main__':
    main()
