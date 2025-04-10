import socket
import cv2
import pickle
import struct
import pyaudio

HOST = '0.0.0.0'
VIDEO_PORT = 5001
AUDIO_PORT = 6001

video_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
video_socket.bind((HOST, VIDEO_PORT))
video_socket.listen(5)

audio_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
audio_socket.bind((HOST, AUDIO_PORT))
audio_socket.listen(5)

print("Esperando conexiones...")
video_conn, _ = video_socket.accept()
audio_conn, _ = audio_socket.accept()
print("Clientes conectados.")

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, output=True, frames_per_buffer=1024)

while True:
    # Recibir video
    data = b""
    while len(data) < struct.calcsize("Q"):
        packet = video_conn.recv(4096)
        if not packet:
            break
        data += packet

    packed_msg_size = data[:struct.calcsize("Q")]
    msg_size = struct.unpack("Q", packed_msg_size)[0]
    data = data[struct.calcsize("Q"):]

    while len(data) < msg_size:
        data += video_conn.recv(4096)

    frame = pickle.loads(data)
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
    cv2.imshow("Video", frame)

    # Recibir audio
    audio_data = audio_conn.recv(1024)
    stream.write(audio_data)

    if cv2.waitKey(1) == 27:
        break

video_conn.close()
audio_conn.close()
cv2.destroyAllWindows()
stream.stop_stream()
stream.close()
p.terminate()
