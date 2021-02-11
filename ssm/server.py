"""server
"""

import os
import struct
import pickle
import socket

import cv2
from Xlib.display import Display


class ScreenMirrorServer:
    def __init__(self, host: str = '', port: int = 7890):
        self._HOST = host
        self._PORT = port

        self._WIDTH, self._HEIGHT = self._screen_size()

        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.bind((self._HOST, self._PORT))

    def start(self):
        self._server_socket.listen()
        conn_socket, addr = self._server_socket.accept()

        self._receive(conn_socket, addr)

    def _receive(self, conn_socket: socket.socket, addr: (str, int)):
        assert (conn_socket is not None)

        overhead_size = struct.calcsize('>III')
        payload_bin = b''

        try:
            while True:
                while len(payload_bin) < overhead_size:
                    received_data_bin = conn_socket.recv(8192)
                    if not received_data_bin:
                        raise StopIteration
                    payload_bin += received_data_bin

                packed_payload_size = payload_bin[:overhead_size]
                payload_bin = payload_bin[overhead_size:]

                width, height, payload_size = struct.unpack('>III', packed_payload_size)

                while len(payload_bin) < payload_size:
                    received_data_bin = conn_socket.recv(8192)
                    if not received_data_bin:
                        raise StopIteration
                    payload_bin += received_data_bin

                encoded_screen_pkl = payload_bin[:payload_size]
                payload_bin = payload_bin[payload_size:]

                encoded_screen = pickle.loads(encoded_screen_pkl)
                screen = cv2.imdecode(encoded_screen, flags=cv2.IMREAD_COLOR)

                if (self._WIDTH < width) and (self._HEIGHT < height):
                    screen = cv2.resize(screen, (self._WIDTH, self._HEIGHT), interpolation=cv2.INTER_AREA)

                cv2.imshow(winname=f'{addr}', mat=screen)
                if cv2.waitKey(1) == 27:
                    raise StopIteration
        except StopIteration:
            conn_socket.close()
            cv2.destroyWindow(winname=f'{addr}')
            print('Mirroring ends...')

    def _screen_size(self) -> (int, int):
        display = Display(display=os.environ['DISPLAY'])
        width, height = display.screen().width_in_pixels, display.screen().height_in_pixels
        return width, height
