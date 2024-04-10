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