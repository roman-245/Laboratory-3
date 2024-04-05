import socket
import struct
import json

def send_data(server_host, server_port):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_host, server_port))

    file_extension = input("Введите расширения для файлов (введите json или xml): ")
    if (file_extension != "json") and (file_extension != "xml"):
        print("Ошибка! Расширение выбрано не правильно, должно быть json или xml.")
        sock.close()
            
    sock.send(file_extension.encode())

    numbers = []
    while True:
        user_input = input("Введите число (или пустую строку для завершения): ")
        if not user_input:
            break

        number = int(user_input)
        numbers.append(int(number))

    # Упаковываем список целых чисел
    data_packed = struct.pack(f'{len(numbers)}i', *numbers)

    sock.sendall(data_packed)

    sock.close()

def request_file(server_host, server_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_host, server_port))

    folder_name = input("Название директорий: ") # К примеру 17-03-2024_17-32-55
    file_number = input("Названия получаемого файла: ")

    sock.sendall(folder_name.encode())
    sock.sendall(str(file_number).encode())

    data = sock.recv(1024)
    recv_size0, = struct.iter_unpack('I', data).__iter__().__next__()
    recv_size1, = struct.unpack('I', data[:struct.calcsize('I')])
    print(f'{recv_size0} == {recv_size1}')

    expected_max_string_size = 1024 - struct.calcsize('I')  # то что здесь magic number, не значит, что так надо делать)
    current_extracting_size = recv_size0 if recv_size0 < expected_max_string_size else expected_max_string_size

    _, string_buff = struct.unpack(f'I{current_extracting_size}s', data)

    recv_size0 -= current_extracting_size
    expected_max_string_size = 1024

    while recv_size0 > 0:
        current_extracting_size = recv_size0 if recv_size0 < expected_max_string_size else expected_max_string_size

        data = sock.recv(1024)
        string_buff += struct.unpack(f'{current_extracting_size}s', data)[0]

        recv_size0 -= current_extracting_size

    recv_string = string_buff.decode()
    json_data = json.loads(recv_string)
    with open(file_number + ".json", 'w') as file:
        json.dump(json_data , file, indent=4)

    print(f"Файл {file_number + '.json'} был успешно перенесён")
    
    sock.close()


server_host = 'localhost'
server_port = 9090

# Пример отправки данных на сервер
send_data(server_host, server_port)

# Пример запроса файла с сервера
request_file(server_host, server_port)
