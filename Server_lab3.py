import os
import shutil
import time
import socket
import pickle
import struct
from threading import Thread


server_address = "localhost"
server_port = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
server_socket.bind(('', 65432))
server_socket.listen(5)


def handle_commands(conn):
    data = conn.recv(1024)
    if data.decode() == 'tim': 
        f1 = input('Введите путь к корневой папке: ')
        f2 = input('Введите путь к папке синхронизации: ')
        check_interval = 5
        sync_folders(f1, f2, check_interval)


while True:
    print("Сервер запущен. Ждет присоединения...")
    conn, address = server_socket.accept()
    print("Connected by", address)
    if conn:
        Thread(target=handle_commands, args=(conn,)).start()

