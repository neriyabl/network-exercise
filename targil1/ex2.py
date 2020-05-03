import socket

my_socket = socket.socket()
my_socket.connect(('127.0.0.1', 8820))

for i in range(10):
    message = input('send message:\n')
    my_socket.send(message.encode())
    data = my_socket.recv(1024)
    print('the server sent: ' + data.decode())

my_socket.close()
