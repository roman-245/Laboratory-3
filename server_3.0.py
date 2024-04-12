import os
import socket
import struct
import pickle
import shutil
import time
from threading import Thread
from all_function_server import *

server_host = "localhost"
server_port = 6543

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_host, server_port))
server_socket.listen(5)

def handle_commands(conn):
    data = conn.recv(1024)
    if data.decode() == 'stasy':
        files = received_files(conn)
        directory1 = f'{os.getcwd()}/a'
        directory2 = f'{os.getcwd()}/b'
        synchronize_folders(directory1, directory2, 5, files)





while True:
    print("Сервер запущен. Ждет присоединения...")
    conn, address = server_socket.accept()
    print("Connected by", address)
    Thread(target=handle_commands, args=(conn,)).start()