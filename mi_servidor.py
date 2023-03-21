import struct
import sys
import socket



DIR = "192.168.0.30"
HOST = "localhost"  # 181.46.137.8"
PORT= 5597





def listen_to(self):
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()

        with conn:
            print('Connected by client with ip address: ', addr)
            while True:
                data = conn.recv(1024)
                if data.decode() != "":
                    data = data.decode('utf-8')
                    print("data", data)



