import socket
import pickle
import time
import os
import struct

# Пример использования
server_address = "localhost"
server_port = 65432
interval = 10
src_path = input("Введите путь к корневой папке: ")


def main(path):
    while True:
        data_set = set(os.listdir(path))
        send_set(data_set, server_address, server_port)
        time.sleep(interval)


def send_set(data_set, server_address, server_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((server_address, server_port))
        data = pickle.dumps(data_set)
        data_size = len(data)
        s.send(struct.pack('!I', data_size))
        size = 1024
        sending_count = 0
        while sending_count < data_size:
            send = data[sending_count:sending_count + size]
            s.send(send)
            sending_count += len(send)
            s.sendall(data)
        print("Множество успешно отправлено.")


if __name__ == '__main__':
    main(src_path)















