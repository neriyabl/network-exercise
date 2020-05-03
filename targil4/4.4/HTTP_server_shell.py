# HTTP Server Shell
# Author: Barak Gonen
# Purpose: Provide a basis for Ex. 4.4
# Note: The code is written in a simple way, without classes, log files or other utilities, for educational purpose
# Usage: Fill the missing functions and constants
import os
import socket
from functools import reduce

from http_helpers import *


def get_file_data(filename):
    """ Get data from file """
    with open(filename, 'rb') as file:
        return file.read()


def send_response(client_socket, status_code, optional_headers='', content=None, content_type=None):
    """
    Send Response message to the client
    @type content: bytes
    @type client_socket: socket.socket
    @param client_socket: the client socket to send the message
    @param status_code: the http status code of the message (if need add new statuses to STATUSES in helpers)
    @param optional_headers: any header accept Content-Type and Content-Length
    @param content: the data of the message
    @param content_type: the file or data type
    @return: None
    """
    status_line = f'HTTP/1.1 {status_code} {STATUSES[status_code]}\r\n'.encode()
    headers = optional_headers.encode()
    if not (content is None and content_type is None):
        headers += f'Content-Type: {RESPONSE_TYPES[content_type]}\r\n'.encode()
    if content is not None:
        headers += f'Content-Length: {len(content)}\r\n'.encode()
    print('-----------------------------------------------')
    print(f'send response: {status_code}')
    print('\t' + headers.decode().replace('\r\n', '\n\t'))
    print('-----------------------------------------------')
    client_socket.send(status_line)
    client_socket.send(headers + b'\r\n')
    if content is not None:
        client_socket.send(content)


def get_params(query_params):
    def insert_param(params, param):
        params[param[:param.index('=')]] = param[param.index('=') + 1:]
        return params

    if query_params == '':
        return {}
    return reduce(insert_param, query_params.split('&'), {})


def handle_client_request(resource, client_socket):
    """
    Check the required resource, generate proper HTTP response and send to client
    @type resource: bytes
    @type client_socket: socket.socket
    @param resource: the resource part in the http url
    @param client_socket: the client socket
    @return: None
    """
    url = resource.decode()
    query_params = ''
    if url == '/':
        url = DEFAULT_URL
    if '?' in url:
        query_params = url[url.index('?') + 1:]
        url = url[:url.index('?')]

    if url in REDIRECTION_DICTIONARY:
        send_response(client_socket, 302, 'Location:' + REDIRECTION_DICTIONARY[url])

    elif url in ACTIONS:
        try:
            params = get_params(query_params)
            send_response(client_socket, 200, '', ACTIONS[url](params), 'txt')
        except AssertionError:
            send_response(client_socket, 400, '', b'Missing or Bad Parameters', 'txt')

    elif url in VALID_RESOURCES:
        content = get_file_data(BASE_URL + url)
        send_response(client_socket, 200, '', content, VALID_RESOURCES[url])

    else:
        if os.path.isfile(BASE_URL + url):
            send_response(client_socket, 403)
        elif not os.path.exists(BASE_URL + url):
            send_response(client_socket, 404)
        else:
            send_response(client_socket, 500)


def validate_http_request(request):
    """ Check if request is a valid HTTP request and returns TRUE / FALSE and the requested URL """
    request_lines = request.split(b'\r\n')
    [method, url, version] = request_lines[0].split()
    if not ((method in [b'GET']) & (version == b'HTTP/1.1')):
        return False, ''
    # TODO more checks headers , etc...
    return True, url


def handle_client(client_socket):
    """ Handles client requests: verifies client's requests are legal HTTP, calls function to handle the requests """
    client_request = client_socket.recv(1024)
    print('-----------------------------------------------')
    print('received new request')
    print('\t' + client_request.decode().replace('\r\n', '\n\t'))
    print('-----------------------------------------------')
    valid_http, resource = validate_http_request(client_request)
    if valid_http:
        print('Valid HTTP request')
        handle_client_request(resource, client_socket)
    else:
        print('Error: Not a valid HTTP request')
        send_response(client_socket, 400)

    print('Closing connection')
    client_socket.close()


def main():
    # Open a socket and loop forever while waiting for clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen(10)
    print(f'Listening for connections on port {PORT}')

    while True:
        print('Waiting for new connection')
        client_socket, client_address = server_socket.accept()
        print('New connection received')
        try:
            client_socket.settimeout(SOCKET_TIMEOUT)
            handle_client(client_socket)
        except socket.timeout:
            print('\n---------- time out ----------\n')
            client_socket.close()
        except socket.error:
            send_response(client_socket, 500)
            client_socket.close()


if __name__ == "__main__":
    # Call the main handler function
    main()
