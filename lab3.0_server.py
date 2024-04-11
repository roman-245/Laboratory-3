import os
import socket
import struct
import pickle
import shutil
import time
from threading import Thread

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 655))
server_socket.listen(5)

def handle_commands(conn):
    data = conn.recv(1024)
    if data.decode() == 'stasy':
        while True:
            directory1 = f'{os.getcwd()}/a'
            directory2 = f'{os.getcwd()}/b'
            gap = 5
            synchronize_folders(directory1, directory2, gap)

def received_files(server_address, server_port):
        client_socket, address = server_socket.accept()
        print("Сервер установил подключение с", address)

        data = client_socket.recv(4)
        data_size = struct.unpack('!I', data)
        received_data = b''
        while len(received_data) < data_size:
            received_data += client_socket.recv(1024)
        files = pickle.loads(received_data)
        print("Полученные данные от клиента:", files)

        return received_data



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

while True:
    conn, address = server_socket.accept()
    print("Connected by", address)
    print("Сервер запущен. Ждет присоединения...")
    if conn:
        Thread(target=handle_commands, args=(conn,)).start()
