from scapy.all import *
from scapy.layers.dns import DNS, DNSQR, DNSRR
from scapy.layers.inet import IP, UDP


class DnsQuery:
    def __init__(self, query_data, query_type, result_type):
        """
        init dns query
        @param query_data: the query name to request
        @param query_type: the query type
        @param result_type: the excepted result type in string
        @type query_data: str
        @type query_type: int
        @type result_type: str
        """
        self.query_data = query_data
        self.query_type = query_type
        self.result_type = result_type

    def send_receive_query(self, dns_server='8.8.8.8'):
        """
        send the query and receive the results DNS Resource Records
        @param dns_server:the ip of a local dns server
        @return: list of all rdata from the DNS Resource Records
        """
        pack = IP(dst=dns_server) / UDP() / DNS(qd=DNSQR(qname=self.query_data, qtype=self.query_type))
        result = sr1(pack, verbose=0)
        if (DNS in result) and (DNSRR in result):
            return [result[DNSRR][x].rdata for x in range(result[DNS].ancount)]


def get_dns_server():
    """
    For some reason in my local network the ip 8.8.8.8 not work to send and receive dns requests
    so i write this function to get the ip of the local dns server from the ipconfig
    @return:the ip address of a local dns server
    """
    sys_output = subprocess.check_output('ipconfig -all | findstr DNS', shell=True)
    dns_line = [line for line in sys_output.decode().splitlines() if line.startswith('   DNS Server')][0]
    return dns_line[dns_line.rindex(' ') + 1:]


def handle_query(query: DnsQuery, dns_server_ip='8.8.8.8'):
    """
    get a dns query send and receive the query and then print the results
    @param query: the query data and meta data
    @param dns_server_ip: the ip of the local dns server
    @return: None
    """
    results = query.send_receive_query(dns_server_ip)
    print()
    if (results is None) or (len(results) == 0):
        if query.query_type == 12:
            query.query_data = '.'.join(reversed(query.query_data.split('.')[:4]))
        print(f'fail to get {query.result_type} for \'{query.query_data}\'')
        return
    if type(results[0]) is bytes:
        results = [res.decode() for res in results]
    if len(results) == 1:
        print(f'{query.result_type}:', results[0])
    else:
        print(f'{query.result_type}s:', results[0])
        for result in results[1:]:
            print(f'\t{result}')


def main():
    # try to get the local dns server ip
    try:
        dns_server_ip = get_dns_server()
    except:
        dns_server_ip = '8.8.8.8'
    while True:
        ns_type = input('enter your choice \'mapping\', \'reverse\' or \'exit\':\n')
        if ns_type == 'mapping':
            url = input('enter domain name: ')
            handle_query(DnsQuery(url, 1, 'ip'), dns_server_ip)
        elif ns_type == 'reverse':
            ip = input('enter ip to reverse: ')
            reversed_ip = '.'.join(reversed(ip.split('.')))
            handle_query(DnsQuery(f'{reversed_ip}.in-addr.arpa', 12, 'domain'), dns_server_ip)
        elif ns_type == 'exit':
            break
        else:
            print('this choice note supported')
        print()


if __name__ == '__main__':
    main()
