import socket


def send(my_socket, command):
    """
    send 4 bytes message to the server in the socket
    receive the response and take the data from the response according to the protocol
    4 first bytes is the data length and then is the data
    @param my_socket: the socket
    @param command: the message to send is a command
    @return: just the response data without the first 4 bytes
    """
    my_socket.send(command.encode())
    length = my_socket.recv(4)
    data = my_socket.recv(int(length))
    return data


def connect():
    """
    create connection with the server
    @return: the socket
    """
    my_socket = socket.socket()
    my_socket.connect(('127.0.0.1', 8820))
    return my_socket


def validate_command(command):
    """
    check if command is a valid command
    @param command: the command from the user
    @return: True if valid else False
    """
    return command in ['TIME', 'NAME', 'RAND', 'EXIT']


def main():
    # connect to the server
    my_socket = connect()
    while True:
        command = input('Enter Command \'TIME\', \'NAME\', \'RAND\' or \'EXIT\'\n').upper()
        if not validate_command(command):
            print(f'the command \'{command}\' is not a valid command')
            continue
        if command == 'EXIT':
            my_socket.send(command.encode())
            break
        data = send(my_socket, command)
        print(f'{command}: {data.decode()}')
    my_socket.close()


if __name__ == '__main__':
    main()
