import os
import shutil
import time
import socket
import struct
import pickle

def start_server(server_host, server_port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_host, server_port))
    server_socket.listen(1)
    print("Запуск сервера, ожидание подключения клиента")
    # Подключаем клиента
    client_socket, addr = server_socket.accept()
    print("Сервер установил подключение с", addr)
    # Получаем размер данных от клиента и декодируем их
    res = client_socket.recv(4)
    data_size, = struct.unpack('!I', res)
    received_data = b''
    while len(received_data) < data_size:
        received_data += client_socket.recv(1024)
    files = pickle.loads(received_data)

    print("Полученные данные от клиента:", files)

    client_socket.close()
    server_socket.close()

# Функция для синхронизации папок
def synchronize_folders(directory1, directory2, gap):
    while True:
        files1 = set(os.listdir(directory1))
        files2 = set(os.listdir(directory2))
        add_files = files1 - files2
        remove_files = files2 - files1
        for file in add_files:
            start = os.path.join(directory1, file)
            finish = os.path.join(directory2, file)
            shutil.copy(start, finish)
            print('Файл', file, 'был добавлен')
        for file in remove_files:
            start = os.path.join(directory2, file)
            os.remove(start)
            print('Файл', file, 'был удален')
        time.sleep(gap)


server_host='localhost'
server_port=65432

start_server(server_host, server_port)
synchronize_folders(f'{os.getcwd()}/a', f'{os.getcwd()}/b', 5)