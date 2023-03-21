import socket
from pymongo import MongoClient
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton


import base64
import gridfs
from io import BytesIO


from PIL import Image



class Principal(BoxLayout):
    def __init__(self):
        super(Principal, self).__init__()

        self.add_widget(Muestra_Imagenes())
        self.add_widget(Puredata_a_Bd())
        self.add_widget(Imagenes_a_Bd())
        self.add_widget(Audio_a_Bd())

class Muestra_Imagenes(BoxLayout):
    def __init__(self):
        super(Muestra_Imagenes, self).__init__()
        self.Btn = Button(text= "mostrar imagen")
        self.add_widget(self.Btn)
        self.Btn.bind(on_press = self.add_btn)

    def add_btn(self, *args):

        mi_archivo = ("image/miarchivo900000.tif")
        mi_img = Image.open(mi_archivo)
        mi_img.show()


class Puredata_a_Bd(BoxLayout):
    def __init__(self):
        super(Puredata_a_Bd, self).__init__()
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
                    pucoltach.insert_one({'desde_pd serv': data})
                    print("subido")
                    if not data:
                        break
            finally:
                connection.close()
                print("cerrado")

class Audio_a_Bd(BoxLayout):
    def __init__(self):
        super(Audio_a_Bd, self).__init__()
        self.BtnCon = ToggleButton(text="Enviar Audio")
        self.add_widget(self.BtnCon)
        self.BtnCon.bind(on_release=self.envia_audio)

    def envia_audio(self, Pymongo):
        archivo_audio = r'/home/ale_acosta/Escritorio/pythonProjectkivy22/audio/sonido1.wav'
        fid1 = ""
        # lectura
        with open(archivo_audio, "rb") as archivo_audio:
            audio_codificado = base64.b64encode(archivo_audio.read())

        # Carga a bd
        arch_audio = "Audio subido"
        fs1 = gridfs.GridFS(mi_audio_bd)
        fileid1 = fs1.put(audio_codificado, filename=arch_audio)
        mi_audio_bd.collec_audio.insert_one({"filename": arch_audio, "fileid1": fileid1})

        for item in mi_audio_bd.collec_audio.find({"filename": arch_audio}):
            fid1 = item['fileid1']

        if fid1 != "":
            salida1 = fs1.get(fid1).read()
            print("esto es un archivo de audio", salida1, "fin de archvo de audio")

class Imagenes_a_Bd(BoxLayout):
    def __init__(self):
        super(Imagenes_a_Bd, self).__init__()
        self.BtnCon= ToggleButton(text="Enviar imagen")
        self.add_widget(self.BtnCon)
        self.BtnCon.bind(on_release=self.envia_imagen)

    def envia_imagen(self, Pymongo):
        archivo_imagen = r'/home/ale_acosta/Escritorio/pythonProjectkivy22/image/miarchivo900000.tif'
        fid = ""
        #lectura
        with open(archivo_imagen, "rb") as archivo_imagen:
            codificada = base64.b64encode(archivo_imagen.read())

        #Carga a bd
        arch_img = "Imagen subida"
        fs = gridfs.GridFS(mi_imagen_bd)
        fileid = fs.put(codificada, filename= arch_img)
        mi_imagen_bd.collec_img.insert_one({"filename":arch_img, "fileid":fileid})

        for item in mi_imagen_bd.collec_img.find({"filename":arch_img}):
            fid = item['fileid']

        if fid != "":
            salida = fs.get(fid).read()
            print("Esto es un archivo de imagen", salida, "fin de archvo de imagen")

