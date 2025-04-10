import socket
import cv2
import pickle
import struct
import pyaudio

SERVER_IP = "192.168.1.1"
VIDEO_PORT = 5000
AUDIO_PORT = 6000

video_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
audio_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

cap = cv2.VideoCapture(0)
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)

while True:
    # Capturar video
    ret, frame = cap.read()
    if not ret:
        break

    _, buffer = cv2.imencode('.jpg', frame)
    message = pickle.dumps(buffer)
    video_socket.sendto(message, (SERVER_IP, VIDEO_PORT))

    # Capturar audio
    audio_data = stream.read(1024)
    audio_socket.sendto(audio_data, (SERVER_IP, AUDIO_PORT))

    if cv2.waitKey(1) == 27:
        break

cap.release()
video_socket.close()
audio_socket.close()
stream.stop_stream()
stream.close()
p.terminate()
