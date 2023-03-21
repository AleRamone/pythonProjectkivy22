import socket
import threading
import time
from pymongo import MongoClient
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton

import base64
import gridfs

from PIL import Image

HEADER = 64
SERVER = socket.gethostbyname(socket.gethostname())
DIR = "192.168.0.30"
HOST = "localhost"  # 181.46.137.8"
PORT= 5599
PORT_S = 5560
PORT_T = 5550
ADDR = (SERVER, PORT_T)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
RECIBO = "Enviar touch"

mongohost =  'mongodb+srv://aleramone:julia2009@cluster0.9cqxg.mongodb.net/test' #'mongodb+srv://aleramone:@cluster0.9cqxg.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
#mongodb://localhost'
client = MongoClient(mongohost)         # conecta a mongodb y genera la conexión a una base de datos especifica.
db = client['login']
basetouch = client['dbtouch']           # base de datos donde se guardan datos touch (o de cursor).
coltach= basetouch['coltouch']       # variable en la cual se guarda una base de datos de los datos de usuarios ingresados, la cual es seleccionada desde client (o creada, de no existir)
                                          # base de datos donde se guardan datos touch (o de cursor).
pucoltach= basetouch['puretouch']
bd_img = client['bd_imagenes']
col_img = bd_img['coll_img']
mi_imagen_bd = client.bd_imagen
mi_audio_bd = client.bd_audio

'''
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            cli_pd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            cli_pd.connect((DIR, PORT_S))
            cli_pd.sendto(msg.to_bytes(4, byteorder='little'), (DIR, PORT))
            if msg == DISCONNECT_MESSAGE:
                connected = False
            print(f"[{addr}] {msg}")
            conn.send("Msg received".encode(FORMAT))
            


    
def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

print("[STARTING] server is starting...")
start()

'''

class Principal(BoxLayout):

    def __init__(self):
        super(Principal, self).__init__()
        self.add_widget(Puredata_to_DB())
        self.add_widget(Audio_to_DB())
        self.add_widget(Show_Image())
        self.add_widget(Image_to_DB())

class Puredata_to_DB(BoxLayout):

    def __init__(self):
        super(Puredata_to_DB, self).__init__()
        self.BtnCon= ToggleButton(text="Conectar a PD")
        self.add_widget(self.BtnCon)
        self.BtnCon.bind(on_release=self.escucha)

    def escucha(self, *args):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (HOST, PORT)
        print(f'starting up on {server_address[0]} port {server_address[1]}')
        sock.bind(server_address)
        sock.listen(1)

        while True:
            print('Esperando conexión')
            connection, client_address = sock.accept()
            try:
                print('Cliente conectado:', client_address)
                while True:
                    data = connection.recv(16)
                    data = data.decode("utf-8")
                    data = data.replace('\n', '').replace('\t','').replace('\r','').replace(';','')
                    print(f'recibí {data}')
                    pucoltach.insert_one({'desde_pd servidor': data})
                    print("subido")
                    if not data:
                        break
            finally:
                connection.close()
                print("cerrado")


class Audio_to_DB(BoxLayout):

    def __init__(self):
        super(Audio_to_DB, self).__init__()
        self.BtnCon = ToggleButton(text="Enviar Audio")
        self.add_widget(self.BtnCon)
        self.BtnCon.bind(on_release=self.envia_audio)

    def envia_audio(self, Pymongo):
        archivo_audio = r'/home/ale_acosta/Escritorio/pythonProjectkivy22/audio/mix.wav'
        fid1 = ""

        with open(archivo_audio, "rb") as archivo_audio:       # lectura
            audio_codificado = base64.b64encode(archivo_audio.read())

        arch_audio = "Audio 14 MARZO"     # Carga a bd
        fs1 = gridfs.GridFS(mi_audio_bd)
        fileid1 = fs1.put(audio_codificado, filename=arch_audio)
        mi_audio_bd.collec_audio.insert_one({"filename": arch_audio, "fileid1": fileid1})

        for item in mi_audio_bd.collec_audio.find({"filename": arch_audio}):
            fid1 = item['fileid1']

        if fid1 != "":
            salida1 = fs1.get(fid1).read()
            print("esto es un archivo de audio", salida1, "fin de archvo de audio")


class Show_Image(BoxLayout):

    def __init__(self):
        super(Show_Image, self).__init__()
        self.Btn = Button(text= "Mostrar imagen")
        self.add_widget(self.Btn)
        self.Btn.bind(on_press = self.add_btn)

    def add_btn(self, *args):
        mi_archivo = ("image/imagenmarzo2100000.tif")
        mi_img = Image.open(mi_archivo)
        mi_img.show()


class Image_to_DB(BoxLayout):

    def __init__(self):
        super(Image_to_DB, self).__init__()
        self.TogBtn = ToggleButton(text="Enviar imagen")
        self.add_widget(self.TogBtn)
        self.TogBtn.bind(on_release=self.envia_imagen)

    def envia_imagen(self, Pymongo):
        archivo_imagen = r'/home/ale_acosta/Escritorio/pythonProjectkivy22/image/imagenmarzo2100000.tif'
        fid = ""

        with open(archivo_imagen, "rb") as archivo_imagen:      #lectura
            codificada = base64.b64encode(archivo_imagen.read())

        arch_img = "Imagen subida"              #Carga a bd
        fs = gridfs.GridFS(mi_imagen_bd)
        fileid = fs.put(codificada, filename= arch_img)
        mi_imagen_bd.collec_img.insert_one({"filename":arch_img, "fileid":fileid})

        for item in mi_imagen_bd.collec_img.find({"filename":arch_img}):
            fid = item['fileid']

        if fid != "":
            salida = fs.get(fid).read()
            print("Esto es un archivo de imagen", salida, "fin de archvo de imagen")


class MainApp(App):

    title= "Servidor"

    def build(self):
        return Principal()

if __name__ == "__main__":
    MainApp().run()
