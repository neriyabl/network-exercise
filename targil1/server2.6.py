import random
import socket
from datetime import datetime

# this dictionary mach between command and
command_controller = {
    b'TIME': lambda: datetime.now().strftime('%c'),
    b'NAME': lambda: 'awesome server',
    b'RAND': lambda: str(int((random.random() * 10) + 1))
}


def validate_command(command):
    """
    validate if command that received is a valid command
    @param command: the received command
    @return: True if the command is valid else False
    """
    return command in command_controller


def send(client_socket, data):
    """
    send data to client first 4 byte for the length of data and then the data
    @param client_socket: the client socket to send the data
    @param data: the data as string
    """
    client_socket.send(str(len(data)).zfill(4).encode())
    client_socket.send(data.encode())


def main():
    # open socket
    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0', 8820))
    server_socket.listen(1)

    try:
        while True:
            # serve new client
            (client_socket, client_address) = server_socket.accept()
            print(f'accept client {client_address}')
            while True:
                # receive command
                command = client_socket.recv(4).upper()
                print(f'receive command {command}')
                if command == b'EXIT':
                    print(f'close client {client_address}')
                    client_socket.close()
                    break
                elif validate_command(command):
                    send(client_socket, command_controller[command]())
                else:
                    send(client_socket, 'not a valid command!')
    finally:
        server_socket.close()


def test():
    assert validate_command(b'') is False
    assert validate_command(b'TIMEX') is False
    assert validate_command(b'RAND') is True
    dummy_socket = type('', (object,), {'send': lambda self, data: self.message.append(data), 'message': []})()
    send(dummy_socket, 'test message')
    assert b''.join(dummy_socket.message) == b'0012test message'
    dummy_socket.message = []
    send(dummy_socket, '')
    assert b''.join(dummy_socket.message) == b'0000'


if __name__ == '__main__':
    test()
    main()
