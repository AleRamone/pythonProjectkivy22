import socket

HEADER = 64
PORT = 5550
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "EL CLIENTE SE HA DESCONECTADO"
SERVER = "127.0.1.1"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

send("Hola desde el cliente!")
input()
send("Envio segundo mensaje")
input()
send("Chau, servidor!")

send(DISCONNECT_MESSAGE)
