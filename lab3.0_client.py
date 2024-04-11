import os
import socket
import struct
import pickle



def send_data(server_host, server_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_host, server_port))

    sock.sendall("stasy".encode())

    data = set(os.listdir(f'{os.getcwd()}/a'))
    # Кодируем данные с помощью pickle
    encoded_data = pickle.dumps(data)
    data_size = len(encoded_data)
    sock.send(struct.pack('!I', data_size))
    chunk_size = 1024
    total_sent = 0
    while total_sent < data_size:
        to_send = encoded_data[total_sent:total_sent + chunk_size]
        sock.send(to_send)
        total_sent += len(to_send)

    print("Данные отправлены на сервер")

    

server_host = 'localhost'
server_port = 65432

send_data(server_host, server_port)

request_file(server_host, server_port)
