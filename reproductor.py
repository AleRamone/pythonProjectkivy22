import pyaudio
import librosa
import wave
'''
MI_AUDIO = 'mis_descargas/mi_audiooo1'
data, sr = librosa.load(MI_AUDIO, sr=22050)
print(data.shape, sr)

import matplotlib.pyplot as plt
import librosa.display

plt.figure(figsize=(14, 5))
librosa.display.waveshow(data, sr=sr)

x = librosa.stft(data)
xdb = librosa.amplitude_to_db(abs(x))

plt.figure(figsize=(14, 5))
librosa.display.specshow(xdb, sr=sr, x_axis= 'time', y_axis='hz')
plt.colorbar()

'''
dur = 15
archivo = "ejemploograba.wav"

audio= pyaudio.PyAudio()


stream=audio.open(format = pyaudio.paInt16,channels=2,rate=44100,input=True, frames_per_buffer=1024)

print("Grabando!")
frames=[]

for i in range(0, int(44100/1024*dur)):
    data=stream.read(1024)
    frames.append(data)

print("Stop--")

stream.stop_stream()
stream.close()
audio.terminate()

wavefile = wave.open(archivo, 'wb')
wavefile.setnchannels(2)
wavefile.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
wavefile.setframerate(44100)
wavefile.writeframes(b''.join()(frames))
wavefile.close()
