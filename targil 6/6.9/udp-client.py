import socket

IP = '10.7.10.37'
PORT = 8821


def main():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    my_socket.sendto(b'aksjkjas', (IP, PORT))
    (data, remo
     te_address) = my_socket.recvfrom(1024)

    print('the server sent: ' + data.decode())
    my_socket.close()


if __name__ == '__main__':
    main()
