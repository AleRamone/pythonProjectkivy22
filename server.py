'''import socket

s = socket.socket()
host = socket.gethostname()
port = 5555
s.bind((host, port))

s.listen(5)
while True:
    cli,addr = s.accept()
    print("Got connection ", addr)
    cli.send("Meeting is at 10am")
    cli.close()
'''

from PIL import Image
