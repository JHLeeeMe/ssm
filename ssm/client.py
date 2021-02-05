"""client
"""

import time
import socket
import pickle
import threading


class ScreenMirrorClient:
    def __init__(self, host: str, port: int = 7890):
        self._host = host
        self._port = port
        self._client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def _send(self):
        while True:
            try:
                data = 'Hello, Socket!'
                b_data = pickle.dumps(data)
                self._client_socket.sendall(b_data)

                time.sleep(1)
            except Exception as e:
                print(e)
                break

    def start(self):
        self._client_socket.connect((self._host, self._port))
        t = threading.Thread(target=self._send)
        t.start()
        t.join()

