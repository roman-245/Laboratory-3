import os
import shutil
import time
import socket
import pickle
import struct


def receive_set(server_address, server_port):
        print(f"Сервер слушает на {server_address}:{server_port}")
        conn, addr = s.accept()
        print(f"Подключение от {addr}")
        data = conn.recv(4)
        data_size = struct.unpack('!I', data)

        received_set = b''
        while len(received_set) < data_size:
            received_set += s.recv(1024)
        files = pickle.loads(received_set)
        print("Полученные данные от клиента:", files)

        return received_set


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
