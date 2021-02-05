"""server
"""

import time
import socket
import pickle
import threading


class ScreenMirrorServer:
    def __init__(self, host: str, port: int = 7890, conn_limits: int = 5):
        self._HOST = host
        self._PORT = port

        self._lock = threading.Lock()
        self._conn_limits = conn_limits

        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.bind((self._HOST, self._PORT))

    def _recieve(self, conn_socket: socket.socket, addr: (str, int)):
        while True:
            try:
                b_data = conn_socket.recv(1024)
                if b_data == b'':
                    break
                data = pickle.loads(b_data)
                print(f'{addr}: {data}')
            except Exception as e:
                print(e)
                break

        with self._lock:
            self._conn_limits += 1
        print('thread end')

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

            t = threading.Thread(name=f'{addr[1]}', target=self._recieve, args=(conn_socket, addr))
            t.start()
