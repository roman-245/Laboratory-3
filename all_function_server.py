import os
import json
import struct
import pickle
import shutil
import time
import subprocess
import datetime
import xml.etree.ElementTree as ET


# Функции Петра
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


def receiving(folders, conn, today, numbers):
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


def json_sender(folders, index, number, conn):
    try:
        with open(f"{folders[index]}/{number}.json") as f:
            conn.sendall(('файл найден').encode())
            try:
                data = json.load(f)
            except json.decoder.JSONDecodeError:
                print('Ваш файл пуст!')
                data = "empty file"
            sent = 0
            chunk_size = 1024
            while sent < len(data):
                sent += conn.send(bytes((data[sent:sent + chunk_size]), encoding="utf-8"))
    except FileNotFoundError:
        conn.sendall('Указанный файл не найден'.encode())


# Функции Анастасии
def synchronize_folders(directory1, directory2, gap, files):
    while True:
        add_files = files - set(os.listdir(directory2))
        remove_files = set(os.listdir(directory2)) - files
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


def received_files(conn):
    # Receive the size of the data and decode it
    res = conn.recv(4)
    data_size, = struct.unpack('!I', res)
    received_data = b''
    while len(received_data) < data_size:
        received_data += conn.recv(1024)
    files = pickle.loads(received_data)
    print("Полученные данные от клиента:", files)
    return files


# Функции Ивана


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


# Функции Романа



# Функция для создания файла и сохранения данных
def save_data(number, file_extension, directory_name, file_name=None):
    # Если имя файла было не задано аргументом, то присваиваем number как имя
    if not file_name:
        file_name = str(number)
    file_path = directory_name + "/" + file_name + "." + file_extension

    # Создание и заполнение данными файл
    data = {"value": number}

    if file_extension == "json":
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

    elif file_extension == "xml":
        root = ET.Element("data")
        root.text = str(data)
        tree = ET.ElementTree(root)
        tree.write(file_path, encoding="utf-8", xml_declaration=True)


# Класс для узлов в дереве
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


# Функция для создания файла, который представляет собой дерево
def build_binary_tree(nums):
    if not nums:
        return None

    root = Node(nums[0])
    queue = [root]
    i = 1

    while i < len(nums):
        # Полученние текущей ссылки для класса
        current_node = queue.pop(0)

        # Добавление слева
        left_value = nums[i] if i < len(nums) else None
        if left_value is not None:
            current_node.left = Node(left_value)
            queue.append(current_node.left)

        i += 1

        # Добавление справа
        right_value = nums[i] if i < len(nums) else None
        if right_value is not None:
            current_node.right = Node(right_value)
            queue.append(current_node.right)

        i += 1

    return root


# Функция для получения данных с дерева рекурсивно
def convert_tree_to_json(root):
    if not root:
        return None

    tree_dict = {}
    tree_dict['value'] = root.value
    tree_dict['left'] = convert_tree_to_json(root.left)
    tree_dict['right'] = convert_tree_to_json(root.right)

    return tree_dict


def create_directory():
    # Текущае время
    now = datetime.datetime.now()
    directory_name = f"{now:%d-%m-%Y_%H-%M-%S}"

    # Создание директории
    os.mkdir(directory_name)
    return directory_name


def received_files(conn):
    # Receive the size of the data and decode it
    res = conn.recv(4)
    data_size, = struct.unpack('!I', res)
    received_data = b''
    while len(received_data) < data_size:
        received_data += conn.recv(1024)
    files = pickle.loads(received_data)
    print("Полученные данные от клиента:", files)
    return files

    # функции Тимофея



def sync_folders(folder1, folder2, interval):
    while True:
        # Get the list of files in both folders
        files1 = set(os.listdir(folder1))
        files2 = set(os.listdir(folder2))

        print(f'Содержимое папки сервера: {files1}')
        print(f'Содержимое папки клиента: {files2}')

        # Find files to be added or removed in folder2
        to_add = files1 - files2
        to_remove = files2 - files1

        # Add missing files from folder1 to folder2
        for file in to_add:
            src = os.path.join(folder1, file)
            dst = os.path.join(folder2, file)
            shutil.copy(src, dst)
            print(f"Added: {file}")

        # Remove extra files from folder2
        for file in to_remove:
            src = os.path.join(folder2, file)
            os.remove(src)
            print(f"Removed: {file}")

        time.sleep(interval)
