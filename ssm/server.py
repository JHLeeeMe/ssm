"""server
"""

import time
import struct
import socket
import pickle
import threading

import cv2


class ScreenMirrorServer:
    def __init__(self, host: str, port: int = 7890, conn_limits: int = 5):
        self._HOST = host
        self._PORT = port

        if conn_limits < 1:
            self._conn_limits = 1
        else:
            self._conn_limits = conn_limits

        self._lock = threading.Lock()

        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.bind((self._HOST, self._PORT))

    def _recieve(self, conn_socket: socket.socket, addr: (str, int)):
        assert (conn_socket is not None)

        overhead_size = struct.calcsize('>I')
        b_payload = b''

        flag = True
        while flag:
            while len(b_payload) < overhead_size:
                b_received_data = conn_socket.recv(overhead_size)
                if b_received_data == b'':
                    conn_socket.close()
                    with self._lock:
                        self._conn_limits += 1
                    flag = False
                    break
                b_payload += b_received_data

            if not flag:
                break

            b_payload_size = b_payload[:overhead_size]
            b_payload = b_payload[overhead_size:]

            payload_size = struct.unpack('>I', b_payload_size)[0]

            while len(b_payload) < payload_size:
                b_received_data = conn_socket.recv(4096)
                if b_received_data == b'':
                    conn_socket.close()
                    with self._lock:
                        self._conn_limits += 1
                    flag = False
                    break
                b_payload += b_received_data

            if not flag:
                break

            b_img_data = b_payload[:payload_size]
            b_payload = b_payload[payload_size:]

            encoded_data = pickle.loads(b_img_data)
            img_data = cv2.imdecode(encoded_data, cv2.IMREAD_COLOR)
            cv2.imshow(f'{addr}', img_data)

        cv2.destroyWindow(winname=f'{addr}')
        print('Mirroring ends...')

    def start(self):
        self._server_socket.listen()
        while True:
            with self._lock:
                if self._conn_limits <= 0:
                    time.sleep(1)
                    continue

            conn_socket, addr = self._server_socket.accept()
            with self._lock:
                self._conn_limits -= 1

            t = threading.Thread(name=f'{addr[0]}', target=self._recieve, args=(conn_socket, addr))
            t.start()
