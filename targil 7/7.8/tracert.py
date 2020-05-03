import time
from datetime import datetime

from scapy.layers.inet import IP, ICMP
from scapy.sendrecv import sr1
from nslookup_with_scapy import nslookup


def get_address(address):
    if not all(d.isdigit() for d in address.split('.')):
        return nslookup.DnsQuery(address, 1, 'ip').send_receive_query()[0], address
    reversed_ip = '.'.join(reversed(address.split('.')))
    return address, nslookup.DnsQuery(f'{reversed_ip}.in-addr.arpa', 12, 'mapping').send_receive_query()[0].decode()


def main():
    user_input = input('enter the ip:\n')
    ip, host = get_address(user_input)
    print(f'Tracing route to {host} [{ip}]\n')

    set_ttl = 0
    res_pack = None
    failed_count = 0
    while ((res_pack is None) or res_pack[ICMP].type == 11) and failed_count < 20:
        set_ttl += 1
        timestamp = datetime.now()
        res_pack = sr1(IP(dst=ip, ttl=set_ttl) / ICMP(type='echo-request'), verbose=0, timeout=2)
        rtt = (datetime.now() - timestamp).microseconds // 1000
        if res_pack:
            print(set_ttl, f'{rtt} ms', res_pack[IP].src, sep='\t')
        else:
            failed_count += 1
    print('\nTrace complete.')


if __name__ == '__main__':
    main()
