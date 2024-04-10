import json
import socket
import time
import os
from threading import Thread

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('', 65432))
server_socket.listen(5)


def treemaker(numbers, today):
    try:
        numbers[0] = Branch(numbers[0])
        for i in range(1, len(numbers)):
            numbers[i] = new_branch(numbers[0], numbers[i])
        with open(today + '/tree_' + today + '.txt', 'w') as f:
            print('Файл с деревом создан')
            display(numbers[0], 0, f, 0)
    except IndexError:
        print('Хм, должно быть вы передали недостаточно чисел для построения дерева!')


def input(name, today, numbers):
    try:
        int(name)
        with open(today + '/' + name + '.json', 'w') as f:
            print(f'Файл {name} создан')
            numbers.append(int(name))
    except ValueError:
        print('введите число')


def receiving(folders):
    names = []
    while True:
        for name in os.listdir():
            if (len(name)) == 19:
                folders.append(name)
        folders.sort()
        name = conn.recv(10240).decode()
        if name not in ['', 'get']:
            input(name, today, numbers)
            names.append(name)
        elif name == '':
            return names
        elif name == 'get':
            index = int(conn.recv(2).decode())
            folder = conn.recv(2).decode()
            json_sender(folders, index, folder, conn)
            break


class Branch:
    def __init__(self, key):
        self.key = key
        self.l = None
        self.r = None
        self.lvl = 0


def new_branch(root, new_key):
    if root is None:
        root = Branch(new_key)
        return root
    if new_key < root.key:
        root.l = new_branch(root.l, new_key)
    else:
        root.r = new_branch(root.r, new_key)
    return root


def display(root, spaces, f, level):
    if root:
        display(root.r, spaces, f, level + 1)
        f.write(level * 5 * " " + str(root.key) + "\n")
        display(root.l, spaces, f, level + 1)


def json_sender(folders, index, number, client):
    try:
        with open(f"{folders[index]}/{number}.json") as f:
            try:
                data = json.load(f)
                print('файл найден')
            except json.decoder.JSONDecodeError:
                print('Ваш файл пуст!')
                data = "empty file"
            sent = 0
            chunk_size = 1024
            while sent < len(data):
                sent += client.send(bytes((data[sent:sent + chunk_size]), encoding="utf-8"))
    except FileNotFoundError:
        print('Указанный файл не найден')


def handle_commands(conn):
    data = conn.recv(1024)
    if data.decode() == "petr":
        folders = []
        numbers = []
        today = time.strftime('%Y-%m-%d_%H-%M-%S')
        os.mkdir(today)
        receiving(folders)
        treemaker(numbers, today)
        conn.close()
        print('Соединение разорвано\n')


while True:
    conn, address = server_socket.accept()
    print("Connected by", address)
    print("Сервер запущен. Ждет присоединения...")
    Thread(target=handle_commands, args=(conn,)).start()
