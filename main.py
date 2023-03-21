import time
import librosa
import librosa.display
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from pymongo import MongoClient
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.filemanager import MDFileManager
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.core.window import Window
import socket
import struct
import pathlib
import pickle
import json
import sys
import os
import bson
import re
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)
from kivy.utils import platform

import base64
import gridfs

from gridfs import GridFSBucket
from io import BytesIO

from PIL import Image

import numpy as np
import matplotlib.pyplot as plt
import cv2

import pyaudio
import wave

DIR = "localhost"
PORT = 5560
#PORTPD = 5559
mongohost =  'mongodb+srv://aleramone:julia2009@cluster0.9cqxg.mongodb.net/test'
#'mongodb+srv://aleramone:@cluster0.9cqxg.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
#mongodb://localhost'

#mongodb+srv://aleramone:cbgb1974@cluster0.9cqxg.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'    # ubicación del servidor a través del protocolo de mongodb. En este caso se conecta a localhost, por defecto en el puerto 27017. LLegado el momento de utilizar un servidor real remplazar "localhost" por ip y puerto asignados.
HEADER = 64
PORT_T = 5550
FORMAT = 'utf-8'
SERVER = "127.0.1.1"   #peticion a servidor

client = MongoClient(mongohost)         # conecta a mongodb y genera la conexión a una base de datos especifica.
db = client['login']                    # variable en la cual se guarda una base de datos de los datos de usuarios ingresados, la cual es seleccionada desde client (o creada, de no existir)
basetouch = client['dbtouch']           # base de datos donde se guardan datos touch (o de cursor).
coltach= basetouch['coltouch']
mi_audio_bd = client.bd_audio
mi_imagen_bd = client.bd_imagen   # colección donde se alojan los documentos con los datos touch.

mmovex = 0
mmovey = 0                             # variables globales utilizadas para almacenar eventos touch para luego guardarlos en los doumentos json.
ddownx= 0
ddowny= 0
uupy= 0
uupx= 0
list_mx = []                          # listas para plotear datos
list_my = []
list_a = []

class MainWindow(Screen):                                       # se instancia la clase mainwindows en la cual tendrá lugar el login de usuarios

    username = ObjectProperty(None)                             # a través de la función id de labels creados en .kv se llama a la s propiedades de tales objetos.
    mail = ObjectProperty(None)
    password = ObjectProperty(None)

    def btn(self):                                              # se convierte a texto los datos ingresados en los labels de .kv para ser almacenados en la colección "users"
        user = self.username.text
        usermail = self.mail.text
        userpswrd = self.password.text
        colle = db['users']
        colle.insert_one({'name': user, 'mail': usermail, 'password': userpswrd})
        print(self.username.text)
        self.username.text = ""
        self.mail.text = ""
        self.password.text = ""


class SecondWindow(Screen, FloatLayout):

    def btn1(self):                                                   #se define un objeto (botón) con un metodo que muestre la ventana popup donde se dara contexto a los eventos de la clase Touch
        show_popup()

    def btnfind(self):                                               #se define un objeto (botón) con metodo para devolver los eventos touch almacenados en documentos json a través de la conexión a mongodb
        datadraw = client.dbtouch.coltouch.find({})

        for documento in datadraw:
            print(documento)

    def btndelete(self):                                                 #se define un objeto (botón) para eliminar los eventos touch almacenados en documentos json en mongodb
        client.dbtouch.coltouch.drop()
        print("Has removidos los datos de BD")

    def plot_list(self):
        from matplotlib import pyplot as plt
        plt.plot(list_mx, list_my)
        print(list_a)
        plt.show()                                                      #plotea datagrama

        my_path = "mis_descargas/lista.txt"                             #archivo .txt
        f = open("archivo.txt", "a+")

        for i in list_a :
            f.write(" ".join(map(str, i)))
        f.close()


class Touch(Widget):                                                                                                         # se instancia la clase Touch para registrar los eventos touch o de cursor en una pantalla popup utlizada como contexto o "pad".

    def on_touch_move(self, touch):

        global mmovex                                                                                                          #se utiliza para llamar a la variable global. Si bien es reconocida por estar declarada al inicio, si no la llamamos inicializará en cero y solo guardará el ultimo evento.
        global mmovey
        mmovex = touch.x
        mmovey = touch.y

        list_mx.append(mmovex)
        list_my.append(mmovey)
        list_a.append(list_mx)
        list_a.append(list_my)

        print("move x", mmovex, "move y", mmovey)

        coltach.insert_one({'movex': mmovex, 'movey': mmovey})
        cli = socket.socket()
        cli = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        cli.connect((DIR, PORT))
        pause_mx = 0.6

        #for base in coltach.find({}, {}):

        for base in coltach.find():                                                             #.sort([('movex', 1)]).limit(1):

            dat = (base.get('movex'))

            if dat != None:


                dato = int(float(dat))
                print("Dato_mx", dato)
                #cli.send(mmovex2)
                cli.sendto(dato.to_bytes(4, byteorder='little'), (DIR, PORT))
                time.sleep(pause_mx)

        for base_my in coltach.find():

            dat_my = (base_my.get('movey'))

            if dat_my != None:
                dato_my1 = int(float(dat_my))
                print("Dato_my", dato_my1)
                cli.sendto(dato_my1.to_bytes(4, byteorder='big'), (DIR, PORT))
                time.sleep(pause_mx)

        cli.close()

    def on_touch_down(self, touch):
        global ddownx
        global ddowny
        ddowny = touch.y
        ddownx = touch.x
        print("down y: ", ddowny, "down x: ", ddownx)
        coltach.insert_one({"down y: ": ddowny, "down x: ": ddownx}) # se guardan uno a uno, en un documento bson, los eventos touch down almacenados en las variables.
        pause_d = 0.65
        cli_d = socket.socket()
        cli_d = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        cli_d.connect((DIR, PORT))

        for base_d in coltach.find():
            dat_d = (base_d.get("down x: "))
            '''
            try:
                if dat_d == float(dat_d):
                    mens = struct.pack('f', dat_d)
                    mens = mens * 50
                    # mens = mens.decode("utf-8")
                    addr = (DIR, PORT)
                    cli_d.sendto(mens, addr)
                    print("touch down es float", mens)
                    time.sleep(pause)
                elif dat_d == str(dat_d):
                    mens = struct.pack('s', dat_d)
                    # mens = mens.decode("utf-8")
                    addr = (DIR, PORT)
                    cli_d.sendto(mens, addr)
                    print("touch down es string", mens)
                    time.sleep(pause)
                

            

            except:
                dat_d == None
                
                '''

            if dat_d != None:
                dato_d = int(float(dat_d))
                print("Dato_d", dato_d)
                cli_d.sendto(dato_d.to_bytes(6, byteorder='big'), (DIR, PORT))
                #time.sleep(pause_d)
        cli_d.close()

    def on_touch_up(self, touch):
        global uupx
        global uupy
        uupy = touch.y
        uupx = touch.x
        print("up x: ", uupy, "up y: ", uupx)
        coltach.insert_one({"up_y": uupy, "up x": uupx})  # se guardan uno a uno, en un documento bson, los eventos touch up almacenados en las variables.


        pause_u = 0.8
        cli_u = socket.socket()

        cli_u = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        cli_u.connect((DIR, PORT))

        for base_u in coltach.find():

            dat_u = (base_u.get("up x"))

            if dat_u != None:
                    dato_u = int(float(dat_u))
                    if dato_u  < 300:
                        print("Dato_u", dato_u)
                        cli_u.sendto(dato_u.to_bytes(8, byteorder='big'), (DIR, PORT))
                        time.sleep(pause_u)
        cli_u.close()


class Pop(FloatLayout):

    global show_popup
    def show_popup():                   # Se define propiedades y metodo de un objeto ventana popup para la clase Pop (es global para que se defina cuando es llamada por el objeto boton btn1 de la clase secondwindows)
        show = Pop()
        popupWindow = Popup(title="touch", content=show, size_hint=(None, None), size=(400, 400))
        popupWindow.open()
        pause = 0.5


class AudioScreen(Screen, FloatLayout):

    def recv_audio(self, *args):
        fs = gridfs.GridFS(mi_audio_bd)
        arch_audio = "Audio 14 MARZO"
        data1 = mi_audio_bd.fs.files.find_one({"filename": arch_audio})
        print(data1)

        mi_id = data1['_id']
        outputdata = fs.get(mi_id).read()
        data2 = np.frombuffer(base64.b64decode(outputdata), np.uint8)
        output = open('mis_descargas/mi_audio_mix', 'wb')
        output.write(data2)
        output.close()
        print("descarga completa", output)

    def open_audio(self):
        chunk = 1024
        f = wave.open(r'mis_descargas/mi_audio_mix', "rb") # ABRIMOS UBICACIÓN DEL AUDIO
        p = pyaudio.PyAudio()  # INICIAMOS PyAudio
        stream = p.open(format=p.get_format_from_width(f.getsampwidth()),  # ABRIMOS STREAM
                        channels=f.getnchannels(),
                        rate=f.getframerate(),
                        output=True)
        data = f.readframes(chunk)  # LEEMOS INFORMACIÓN

        while data:                   # REPRODUCIMOS "stream"
            stream.write(data)
            data = f.readframes(chunk)
        stream.stop_stream() # PARAMOS "stream".
        stream.close()
        p.terminate()  # FINALIZAMOS PyAudio

    def plot_audio(self):
        MI_AUDIO = 'mis_descargas/mi_audio_mix'
        import matplotlib.pyplot as plt
        data, sr = librosa.load(MI_AUDIO, sr=44100)
        print(data.shape, sr)

        try:
            plt.figure(figsize=(14, 5))
            plt.subplot(3, 1, 1)
            librosa.display.waveshow(data, sr=sr)
            plt.savefig("mis_descargas/mi_forma_mix.jpg")
            plt.show()
            archivo_imagen = r'/home/ale_acosta/Escritorio/pythonProjectkivy22/mis_descargas/Forma_de_onda_1.jpg'
            fid = ""

            with open(archivo_imagen, "rb") as archivo_imagen:         # lectura
                codificada = base64.b64encode(archivo_imagen.read())

            arch_img = "Forma de onda mix subida"      # Carga a bd
            fs = gridfs.GridFS(mi_imagen_bd)
            fileid = fs.put(codificada, filename=arch_img)
            mi_imagen_bd.collec_ondas.insert_one({"filename": arch_img, "fileid": fileid})

        finally:
                print('Hemos ploteado una forma de onda!')

    def plot_spectrum(self):

        MI_AUDIO = 'mis_descargas/mi_audio_mix'
        import matplotlib.pyplot as plt
        data, sr = librosa.load(MI_AUDIO, sr=44100)
        print(data.shape, sr)

        try:
            x = librosa.stft(data)
            xdb = librosa.amplitude_to_db(abs(x))

            plt.figure(figsize=(14, 5))
            librosa.display.specshow(xdb, sr=sr, x_axis='time', y_axis='hz')

            plt.colorbar()
            plt.savefig("mis_descargas/Ejemplo_espectro_mix.jpg")
            plt.show()

            archivo_imagen = r'/home/ale_acosta/Escritorio/pythonProjectkivy22/mis_descargas/Ejemplo_espectro_1.jpg'
            fid = ""

            with open(archivo_imagen, "rb") as archivo_imagen:         # lectura
                codificada = base64.b64encode(archivo_imagen.read())

            arch_img = "Espectro mix subido"        # Carga a bd
            fs = gridfs.GridFS(mi_imagen_bd)
            fileid = fs.put(codificada, filename=arch_img)
            mi_imagen_bd.collec_espectros.insert_one({"filename": arch_img, "fileid": fileid})

        finally:
                print('Hemos ploteado el espectro!')

    def record_audio(self):

        dur = 10
        archivo = "miaudio2.wav"
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16, channels=2, rate=44100, input=True, frames_per_buffer=1024)

        print("Grabando! ⚫")

        frames = []

        for i in range(0, int(44100 / 1024 * dur)):
            data = stream.read(1024)
            frames.append(data)

        print("Stop  ■ ")

        stream.stop_stream()
        stream.close()
        audio.terminate()

        wavefile = wave.open(archivo, 'wb')
        wavefile.setnchannels(2)
        wavefile.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        wavefile.setframerate(44100)
        wavefile.writeframes(b''.join(frames))
        wavefile.close()
    
    def upload_audio(self):
    
        audio_f = r'/home/ale_acosta/Escritorio/pythonProjectkivy22/miaudio2.wav'
        fid_rec = ""

        with open(audio_f, "rb") as audio_f:                   # lectura
            audio_codif = base64.b64encode(audio_f.read())


        my_audio_rec = "Grabación subida"        # Carga a bd
        fs1 = gridfs.GridFS(mi_audio_bd)
        fileid1 = fs1.put(audio_codif, filename=my_audio_rec)
        mi_audio_bd.collec_record.insert_one({"filename": my_audio_rec, "fileid1": fileid1})

        for item in mi_audio_bd.collec_record.find({"filename": my_audio_rec}):
            fid_rec = item['fileid1']

        if fid_rec != "":
            salida1 = fs1.get(fid_rec).read()
            print("esto es un archivo de audio", salida1, "fin de archvo de grabación")

class ImagenScreen(Screen, FloatLayout):

    def recv_image(self, *args):

        arch_imagen = "Imagen subida"        # mismas vaiables que al subir audio
        fs = gridfs.GridFS(mi_imagen_bd)

        const_img = fs.find_one({"filename":arch_imagen})     #construcción de imagen
        leer_img = const_img.read()

        data =np.frombuffer(base64.b64decode(leer_img), np.uint8)
        img_cv2 = cv2.imdecode(data, 3)
        img_cv2 = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2RGB)
        plt.imshow(img_cv2)
        plt.show()

    def send_img_pd(self, *args):

        pause = 0.8
        imagen = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        imagen.connect((DIR, PORT))
        #img = Image.open(".../image/broco.png")
        #img.show()
        #filename1 = "image/broco.png"
        #imag1 = Image.open(filename1)
        #imag1.show()
        file = open("image/broco.png", "rb")

        content = file.readlines(4096)

        for i in content:
            time.sleep(pause)
            cont = i*30
            #print(type(i))
            #imagen.sendto(cont.to_bytes(8, byteorder='little'), (LIP, PORT))
            imagen.sendall(cont)

            print(cont)
            file.close()

    def send_image(self):
        archivo_imagen = r'/home/ale_acosta/Escritorio/pythonProjectkivy22/image/miarchivo900000.tif'
        fid = ""

        with open(archivo_imagen, "rb") as archivo_imagen:            # lectura
            codificada = base64.b64encode(archivo_imagen.read())

            arch_img = "subida por cliente"     # Carga a bd
            fs = gridfs.GridFS(mi_imagen_bd)
            fileid = fs.put(codificada, filename=arch_img)
            mi_imagen_bd.collec_img.insert_one({"filename": arch_img, "fileid": fileid})

            for item in mi_imagen_bd.collec_img.find({"filename": arch_img}):
                fid = item['fileid']

            if fid != "":
                salida = fs.get(fid).read()
                print("Esto es un archivo de imagen", salida, "fin de archvo de imagen")


class WindowManager(ScreenManager):

    def on_enter(self, *args):

        if platform == 'android':
            request_permissions([
                Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE
            ])

kv = Builder.load_file("my.kv")     # se asigna un metodo a la clase  Builder para cargar el archivo kv cuando la variable ea retornada en la instancia mymainapp

class MyMainApp(App):

    title = "Cliente"
    def build(self):
        Window.size = [300, 600]
        return kv

if __name__ == "__main__":

    MyMainApp().run()

