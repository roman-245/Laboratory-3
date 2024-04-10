import datetime
import os
import socket
import struct
import xml.etree.ElementTree as ET
import json

# Функция для создания директорий
def create_directory():
    # Текущае время
    now = datetime.datetime.now()
    directory_name = f"{now:%d-%m-%Y_%H-%M-%S}"

    # Создание директории
    os.mkdir(directory_name)
    return directory_name

# Функция для создания файла и сохранения данных
def save_data(number, file_extension, directory_name, file_name = None):
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

# Главная фукция для запуска программы
def main():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', 9090))
    server_socket.listen(1)

    print("Сервер запущен. Ждет присоединения...")
    while True:

        conn, addr = server_socket.accept()
        print("Присоединился к ", addr)
            
        while True:

            data1 = conn.recv(1024)
            data2 = conn.recv(1024)

            if not data1 or not data2:
                break

            if str(data1.decode()) == "json" or str(data1.decode()) == "xml":

                # Создание директории
                directory_name = create_directory()

                # Расширение для файлов
                file_extension = str(data1.decode())

                # Распаковываем данные обратно в список
                numbers = struct.unpack(f'{len(data2)//4}i', data2)

                for number in numbers:
                    save_data(number, file_extension, directory_name)
                    
                # Строим бинарное дерево
                root_node = build_binary_tree(numbers)

                # Преобразуем дерево в JSON
                json_tree = convert_tree_to_json(root_node)

                # Сохраняем JSON в файл
                with open(f"{directory_name}/binary_tree.json", "w") as file:
                    json.dump(json_tree, file, indent=4)

                print("Бинарное дерево успешно сохранено в файл 'binary_tree.json'")

            else:
                directory = str(data1.decode())
                all_directory = [filename for filename in os.listdir()]

                if directory in all_directory:
                    file_name = str(data2.decode()) + ".json"

                    if file_name in os.listdir(directory):
                        path_to_file = directory + '/' + file_name

                        with open(path_to_file, 'r') as json_file:
                            data = json.load(json_file)
                            string = json.dumps(data)
                            conn.send(struct.pack(f'I{len(string)}s', len(string), string.encode()))
                            #data = json.load(json_file)
                            #conn.send(json.dumps(data).encode())

    server_socket.close()

# Вызываем функцию для создания папки и файлов
if __name__ == "__main__":
    main()