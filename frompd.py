
from pymongo import MongoClient
import socket

mongohost =  'mongodb+srv://aleramone:julia2009@cluster0.9cqxg.mongodb.net/test' #'mongodb+srv://aleramone:@cluster0.9cqxg.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
#mongodb://localhost'
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 5555)
print(f'starting up on {server_address[0]} port {server_address[1]}')
sock.bind(server_address)
sock.listen(1)

client = MongoClient(mongohost)         # conecta a mongodb y genera la conexión a una base de datos especifica.
db = client['login']                    # variable en la cual se guarda una base de datos de los datos de usuarios ingresados, la cual es seleccionada desde client (o creada, de no existir)
basetouch = client['dbtouch']           # base de datos donde se guardan datos touch (o de cursor).
pucoltach= basetouch['puretouch']

while True:
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print('client connected:', client_address)
        while True:
            data = connection.recv(16)
            data = data.decode('utf-8')
            data = data.replace('\n', '').replace('\t', '').replace('\r', '').replace(';', '')

            print(f'received {data}')
            pucoltach.insert_one({'desde_pd enero': data})
            print("subido")
            if not data:
                break
    finally:
        connection.close()