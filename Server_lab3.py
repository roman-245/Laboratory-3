import datetime
import os
import socket
import struct
import xml.etree.ElementTree as ET
import json
from threading import Thread
from all_function_server import *

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('', 65432))
server_socket.listen(5)

# Главная фукция для запуска программы
def handle_commands(conn):
    
    data = conn.recv(1024)
    if data.decode() == "var1":   # Пример ввода варианта - var1
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

                    else:
                        print("Такой файл не существует!")
                        conn.close()

                else:
                    print("Такой директории не существует!")
                    conn.close()

while True:
    conn, address = server_socket.accept()
    print("Connected by", address)
    print("Сервер запущен. Ждет присоединения...")
    Thread(target=handle_commands, args=(conn,)).start()
