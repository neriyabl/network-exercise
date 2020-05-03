#   Heights sockets Ex. 2.7 template - server side
#   Author: Barak Gonen, 2017
import glob
import os
import shutil
import socket

from PIL import ImageGrab

IP = '0.0.0.0'
PORT = 8820
COMMANDS = ['TAKE_SCREENSHOT', 'SEND_FILE', 'DIR', 'DELETE', 'COPY', 'EXECUTE', 'EXIT']


def receive_client_request(client_socket):
    """Receives the full message sent by the client

    Works with the protocol defined in the client's "send_request_to_server" function

    Returns:
        command: such as DIR, EXIT, SCREENSHOT etc
        params: the parameters of the command

    Example: 12DIR c:\cyber as input will result in command = 'DIR', params = 'c:\cyber'
    """
    length = client_socket.recv(2)
    if length.isdigit():
        req = client_socket.recv(int(length))
        command, *params = req.split()
        return command, params


def check_client_request(command, params):
    """Check if the params are good.

    For example, the filename to be copied actually exists

    Returns:
        valid: True/False
        error_msg: None if all is OK, otherwise some error message
    """
    if command in [b'TAKE_SCREENSHOT', b'EXIT']:
        return len(params) == 0, ['this commands not need parameters', None][len(params) == 0]
    elif command in [b'SEND_FILE', b'DIR', b'DELETE', b'EXECUTE']:
        if len(params) != 1:
            return False, b'missing or to much parameters'
        path = params[0]
        if (not os.path.exists(path)) & all(
                [not os.path.exists(f'{p}/{path.decode()}'.replace('\\', '/')) for p in
                 os.environ.get('path').split(';')]):
            print('\n'.join([f'{p}/{path.decode()}'.replace('\\', '/') for p in os.environ.get('path').split(';')]))
            return False, b'the path is not exist'
        if (command in [b'SEND_FILE', b'DELETE', b'EXECUTE']) & (not os.path.isfile(path)) & all(
                [not os.path.isfile(f'{p}/{path.decode()}'.replace('\\', '/')) for p in
                 os.environ.get('path').split(';')]):
            return False, b'the path is not a file'
        return True, None
    elif command == b'COPY':
        if len(params) != 2:
            return False, b'missing or to much parameters'
        if not all(os.path.exists(path) & os.path.isfile(path) for path in params):
            return False, b'some paths are not files or not exists'
        return True, None
    return False, f'\'{command.decode()}\' is not a valid command'.encode()


def handle_client_request(command, params):
    """Create the response to the client, given the command is legal and params are OK

    For example, return the list of filenames in a directory

    Returns:
        response: the requested data
    """
    if command == b'TAKE_SCREENSHOT':
        im = ImageGrab.grab()
        im.save(r'screen.jpg')
        return b'0'
    elif command == b'DIR':
        return b'\n'.join(glob.glob(params[0] + r'\*.*'.encode()))
    path = params[0]
    if not os.path.exists(path):
        path = [f'{p}/{path.decode()}' for p in os.environ.get('path').replace('\\', '/').split(';') if
                os.path.exists(f'{p}/{path.decode()}')][0]
    if command == b'SEND_FILE':
        with open(path, 'rb') as file_to_send:
            return file_to_send.read()
    elif command == b'DELETE':
        os.remove(path)
        return b'0'
    elif command == b'EXECUTE':
        os.startfile(path)
        return b'0'
    elif command == b'COPY':
        shutil.copy(path, params[1])
        return b'0'
    return b''


def send_response_to_client(response, client_socket):
    """Create a protocol which sends the response to the client
x
    The protocol should be able to handle short responses as well as files
    (for example when needed to send the screenshot to the client)
    """
    chunks = [response[x:x + 1024] for x in range(0, len(response), 1024)]

    for index, chunk in enumerate(chunks):
        if index == (len(chunks) - 1):
            client_socket.send(f'0{str(len(chunk)).zfill(4)}'.encode() + chunk)
        else:
            client_socket.send('1'.encode() + chunk)


def send_error_to_client(error_msg, client_socket):
    client_socket.send(f'2{str(len(error_msg)).zfill(4)}'.encode() + error_msg)


def main():
    # open socket with client
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen(1)
    client_socket, address = server_socket.accept()

    # handle requests until user asks to exit
    done = False
    while not done:
        command, params = receive_client_request(client_socket)
        valid, error_msg = check_client_request(command, params)
        if valid:
            response = handle_client_request(command, params)
            send_response_to_client(response, client_socket)
        else:
            send_error_to_client(error_msg, client_socket)

        if command == 'EXIT':
            done = True

    client_socket.close()
    server_socket.close()


if __name__ == '__main__':
    main()
