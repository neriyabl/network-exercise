#   Heights sockets Ex. 2.7 template - client side
#   Author: Barak Gonen, 2017


import socket

IP = '127.0.0.1'
PORT = 8820
COMMANDS = ['TAKE_SCREENSHOT', 'SEND_FILE', 'DIR', 'DELETE', 'COPY', 'EXECUTE', 'EXIT']


def valid_request(request):
    """Check if the request is valid (is included in the available commands)

    Return:
        True if valid, False if not
    """
    return (request.split()[0].upper() in COMMANDS) & len(request) < 100


def send_request_to_server(my_socket, request):
    """Send the request to the server. First the length of the request (2 digits), then the request itself

    Example: '04EXIT'
    Example: '12DIR c:\cyber'
    """
    length = len(request)
    my_socket.send((str(length).zfill(2) + request).encode())


def handle_server_response(my_socket, request):
    """Receive the response from the server and handle it, according to the request

    For example, DIR should result in printing the contents to the screen,
    while SEND_FILE should result in saving the received file and notifying the user
    """
    more_flag = my_socket.recv(1)
    data = b''
    while more_flag == b'1':
        data += my_socket.recv(1024)
        more_flag = my_socket.recv(1)
    last_pack_size = my_socket.recv(4)
    data += my_socket.recv(int(last_pack_size))
    if more_flag == b'2':
        print(data.decode())
        return

    def successes(_):
        print('command succeeded')

    def send_file(file_name):
        with open('response_file', 'wb') as out_file:
            out_file.write(file_name)
        successes('')

    def print_list(binary_list):
        print(binary_list.decode())
        successes('')

    response_controller = {
        'TAKE_SCREENSHOT': successes,
        'SEND_FILE': send_file,
        'DIR': print_list,
        'DELETE': successes,
        'COPY': successes,
        'EXECUTE': successes
    }
    response_controller[request.split(' ')[0]](data)


def main():
    # open socket with the server
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((IP, PORT))

    # print instructions
    print('Welcome to remote computer application. Available commands are:\n')
    print('\n'.join(COMMANDS))

    done = False
    # loop until user requested to exit
    while not done:
        request = input("Please enter command:\n")
        if valid_request(request):
            send_request_to_server(my_socket, request)
            handle_server_response(my_socket, request)
            if request == 'EXIT':
                done = True
    my_socket.close()


if __name__ == '__main__':
    main()
