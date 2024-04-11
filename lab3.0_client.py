import os
import socket
import struct
import pickle

def send_data_to_server(server_host, server_port, directory):

    # Устанавливаем порт и создаем клиентский сокет
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_host, server_port))
    # Получаем список файлов в указанной директории
    data = set(os.listdir(directory))
    # Кодируем данные с помощью pickle
    encoded_data = pickle.dumps(data)
    data_size = len(encoded_data)
    # Отправляем размер данных на сервер
    client_socket.send(struct.pack('!I', data_size))
    # Отправляем данные по частям
    chunk_size = 1024
    total_sent = 0
    while total_sent < data_size:
        to_send = encoded_data[total_sent:total_sent + chunk_size]
        client_socket.send(to_send)
        total_sent += len(to_send)
    print("Данные отправлены на сервер")
    # Закрываем соединение
    client_socket.close()


server_host='localhost'
server_port=65432
directory1 = f'{os.getcwd()}/a'

# Вызов функции с указанием пути к директории
send_data_to_server(server_host, server_port, directory1)