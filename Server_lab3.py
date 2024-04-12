import json
import socket
import time
import os
from threading import Thread
from all_function_server import *

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('', 65432))
server_socket.listen(5)


def handle_commands(conn):
    data = conn.recv(1024)
    if data.decode() == "petr":
        folders = []
        numbers = []
        today = time.strftime('%Y-%m-%d_%H-%M-%S')
        os.mkdir(today)
        receiving(folders, conn, today, numbers)
        treemaker(numbers, today)
        conn.close()
        print('Соединение разорвано\n')
    else:
        print('введите существующий вариант')


while True:
    conn, address = server_socket.accept()
    print("Connected by", address)
    print("Сервер запущен. Ждет присоединения...")
    Thread(target=handle_commands, args=(conn,)).start()
