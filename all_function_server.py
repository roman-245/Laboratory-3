import os
import socket
import struct
import pickle
import shutil
import time

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