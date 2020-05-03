from scapy.all import *
from scapy.layers.inet import UDP, IP

ip = '0.0.0.0'


def main():
    message = input('enter your message: ')
    for char in message:
        char_port = ord(char)
        my_pack = IP(dst=ip) / UDP(dport=char_port)
        send(my_pack)


if __name__ == '__main__':
    main()
