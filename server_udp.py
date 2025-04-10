import socket
import cv2
import pickle
import struct
import pyaudio

# Configuración del servidor
HOST = '0.0.0.0'
VIDEO_PORT = 5000
AUDIO_PORT = 6000

# Sockets para video y audio
video_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
video_socket.bind((HOST, VIDEO_PORT))

audio_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
audio_socket.bind((HOST, AUDIO_PORT))

# Configuración de audio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, output=True, frames_per_buffer=1024)

print("Servidor UDP esperando clientes...")

while True:
    # Recibir video
    packet, client_addr = video_socket.recvfrom(65536)
    frame = pickle.loads(packet)
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
    cv2.imshow("Video", frame)

    # Recibir audio
    audio_data, _ = audio_socket.recvfrom(1024)
    stream.write(audio_data)

    if cv2.waitKey(1) == 27:
        break

video_socket.close()
audio_socket.close()
cv2.destroyAllWindows()
stream.stop_stream()
stream.close()
p.terminate()
