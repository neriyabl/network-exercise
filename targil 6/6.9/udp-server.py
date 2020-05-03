import socket

IP = '0.0.0.0'
PORT = 8821


def main():
    while True:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.bind((IP, PORT))
        (client_name, client_address) = server_socket.recvfrom(1024)
        server_socket.sendto(client_name, client_address)
    server_socket.close()


if __name__ == '__main__':
    main()
