import datetime
import socket
import json
from threading import Thread
import os
import time
import subprocess
import struct

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('', 65432))
server_socket.listen(5)


# Главная функция для запуска программы
def handle_commands(conn):
    data = conn.recv(1024)
    commands = []
    if data.decode() == "var5":
        while True:
            try:
                command = conn.recv(1024).decode()
                if command == "var5_add_command":
                    new_command = conn.recv(1024).decode()
                    commands.append(new_command)
                    print(commands)
                    run(commands)
                elif command == "var5_get_file":
                    program_name = conn.recv(1024).decode()
                    send_files(conn, program_name)
            except ConnectionResetError:
                print("Подключение оборвалось")
                break
            except Exception as e:
                print(f"Error: {e}")
                break


def run(commands):
    make_dir(commands)
    for command in commands:
        timestamp = time.strftime("%d-%m_%H-%M-%S")
        file_name = os.getcwd() + "/" + command.split(" ")[0] + "/" + f"{timestamp}_output.txt"
        with open(file_name, 'a') as f:
            subprocess.run(command, shell=True, stdout=f)


def make_dir(commands):
    for command in commands:
        directory_name = command.split(" ")
        os.makedirs(directory_name[0], exist_ok=True)


def send_files(conn, program_name):
    path = os.getcwd() + "/" + program_name
    if os.path.exists(path):
        file_list = os.listdir(path)
        for file in file_list:
            with open(path + "/" + file, "rb") as f:
                while True:
                    file_data = f.readline()
                    file_size = len(file_data)
                    conn.send(struct.pack("!I", file_size))
                    conn.send(file_data)
                    if not file_data:
                        break


while True:
    print("Сервер запущен. Ждет присоединения...")
    conn, address = server_socket.accept()
    print("Connected by", address)
    if conn:
        Thread(target=handle_commands, args=(conn,)).start()

