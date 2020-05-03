from scapy.all import *
from scapy.layers.dns import DNS, DNSQR
from scapy.layers.inet import IP, UDP

ip = '0.0.0.0'


def get_word(char):
    word = char
    for i in range(random.randint(3, 5)):
        word += chr(random.randint(97, 122))
    return word


def main():
    message = input('enter your message: ')
    for char in message:
        url = f'www.{get_word(char)}.com'
        print(url)
        send(IP(dst=ip) / UDP(dport=53) / DNS(rd=1, qd=DNSQR(qname=url, qtype="A")))


if __name__ == '__main__':
    main()
