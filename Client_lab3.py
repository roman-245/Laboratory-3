import json
import socket

client = socket.socket()
client.connect(('localhost', 65432))

variant = input("Введите вариант: ")
if variant=='petr':
    client.sendall(variant.encode())

    while True:
        message = input('Введите число')
        if message == '':
            client.send(message.encode())
            break
        elif message == 'get':
            client.send(message.encode())
            index = input('введите индекс папки')
            num = input('введите номер файла')
            client.send(index.encode())
            client.send(num.encode())
            print((client.recv(1024)).decode())
            json_file = client.recv(1024)
            json_file = json_file.decode('UTF-8')
            with open(f"{index}_{num}.json", "w") as f:
                if json_file != 'empty file':
                    try:
                        json.dump(json_file, f)
                        break
                    except json.decoder.JSONDecodeError:
                        print('Произошла непредвиденная ошибка')
                else:
                    print('файл был пустой')
                    break
            print('Попытка передачи файла завершена')

        else:
            client.send(message.encode())
    print('Завершение работы')
    client.close()