import socket
import json
import struct


def response():
    with open('received.txt', 'rb') as f:
        lines = [i.decode('cp1251') for i in f.readlines()]
    print(lines)


class Main2:
    def __init__(self):
        self.host = 'localhost'
        self.port = 65432
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
            self.send('var5')
            print("Подключение к серверу прошло успешно")
        except ConnectionRefusedError:
            print("Подключение не удалось")
        while True:
            print("1 - Отправить команды на сервер\n"
                  "2 - Запросить у сервера файл с выводами команды\n"
                  "3 - Завершить сеанс\n")
            self.option = input("Ваш выбор: ")
            if self.option == "1":
                self.send('var5_add_command')
                command = input("Введите название команды, которую нужно отправить на сервер: ")
                self.client_socket.send(command.encode())
            elif self.option == "2":
                self.send('var5_get_file')
                command = input("Введите название команды, выводы которой нужно получить: ")
                self.client_socket.send(command.encode())
                self.receive()
                response()
            elif self.option == "3":
                self.client_socket.close()
                break
            else:
                print("Выберите представленную опцию: ")

    def send(self, command, data=None):
        self.client_socket.send(command.encode())
        if data:
            self.client_socket.send(data.encode())

    def receive(self):
        file_size = struct.unpack('!I', self.client_socket.recv(4))[0]
        received_data = b''
        while len(received_data) < file_size:
            data = self.client_socket.recv(1024)
            if not data:
                break
            received_data += data
            with open("received.txt", "ab") as f:
                f.write(received_data)


if __name__ == '__main__':
    main2 = Main2()

