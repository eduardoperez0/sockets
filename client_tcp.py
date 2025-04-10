import socket
import cv2
import pickle
import struct
import pyaudio

SERVER_IP = "192.168.1.1"
VIDEO_PORT = 5001
AUDIO_PORT = 6001

video_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
video_socket.connect((SERVER_IP, VIDEO_PORT))

audio_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
audio_socket.connect((SERVER_IP, AUDIO_PORT))

cap = cv2.VideoCapture(0)
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    _, buffer = cv2.imencode('.jpg', frame)
    message = pickle.dumps(buffer)
    video_socket.sendall(struct.pack("Q", len(message)) + message)

    audio_data = stream.read(1024)
    audio_socket.sendall(audio_data)

    if cv2.waitKey(1) == 27:
        break

cap.release()
video_socket.close()
audio_socket.close()
stream.stop_stream()
stream.close()
p.terminate()
