"""server
"""

import time
import struct
import socket
import pickle
import threading

import cv2


class ScreenMirrorServer:
    def __init__(self, host: str = '', port: int = 7890):
        self._HOST = host
        self._PORT = port

        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.bind((self._HOST, self._PORT))

    def start(self):
        self._server_socket.listen()
        conn_socket, addr = self._server_socket.accept()

        t = threading.Thread(target=self._receive, args=(conn_socket, addr))
        t.start()

    def _receive(self, conn_socket: socket.socket, addr: (str, int)):
        assert (conn_socket is not None)

        overhead_size = struct.calcsize('>I')
        payload_bin = b''

        try:
            while True:
                while len(payload_bin) < overhead_size:
                    received_data_bin = conn_socket.recv(overhead_size)
                    if not received_data_bin:
                        raise StopIteration
                    payload_bin += received_data_bin

                packed_payload_size = payload_bin[:overhead_size]
                payload_bin = payload_bin[overhead_size:]

                payload_size = struct.unpack('>I', packed_payload_size)[0]

                while len(payload_bin) < payload_size:
                    received_data_bin = conn_socket.recv(4096)
                    if not received_data_bin:
                        raise StopIteration
                    payload_bin += received_data_bin

                encoded_screen_pkl = payload_bin[:payload_size]
                payload_bin = payload_bin[payload_size:]

                encoded_screen = pickle.loads(encoded_screen_pkl)
                screen = cv2.imdecode(encoded_screen, flags=cv2.IMREAD_COLOR)

                cv2.imshow(winname=f'{addr}', mat=screen)
                if cv2.waitKey(1) == 27:
                    raise StopIteration
        except StopIteration:
            conn_socket.close()
            cv2.destroyWindow(winname=f'{addr}')
            print('Mirroring ends...')

