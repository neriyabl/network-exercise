import socket

server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8820))
server_socket.listen(1)

(client_socket, client_address) = server_socket.accept()

while True:
    client_name = client_socket.recv(1024)
    if client_socket is None:
        break
    client_socket.send('hello ' + client_name)

client_socket.close()
server_socket.close()
