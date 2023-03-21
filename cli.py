import socket

LIP = "192.168.0.30"
PORT = 5560

cli = socket.socket()
cli.connect((LIP, PORT))
cli.send("hola servidor")
respuesta = cli.recv(1024)
print(respuesta)
# cli = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
cli.close()
