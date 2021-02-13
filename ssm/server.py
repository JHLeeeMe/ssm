"""Simple Screen Mirror Server

1. receive screen data from client
2. show client screen

Functions:
    _screen_size() -> (int, int)

Classes:
    ScreenMirrorServer
"""

import os
import struct
import pickle
import socket

import cv2
from Xlib.display import Display


def _screen_size() -> (int, int):
    """Get screen size

    extract screen size in pixels

    Returns:
        width, height: (int, int)
    """
    display = Display(display=os.environ['DISPLAY'])
    width, height = \
        display.screen().width_in_pixels, display.screen().height_in_pixels
    return width, height


class ScreenMirrorServer:
    """ScreenMirrorServer

    Attributes:
        _HOST: str = ''
            client ip (default: all ip)
        _PORT: int = 7890

        _WIDTH: int
            screen x-axis size
        _HEIGHT: int
            screen y-axis size

        _server_socket: socket.socket
            socket (IPv4, TCP)

    Methods:
        start() -> None

        _receive(conn_socket: socket.socket, addr: (str, int)) -> None
    """
    def __init__(self, host: str = '', port: int = 7890):
        self._HOST = host
        self._PORT = port

        self._WIDTH, self._HEIGHT = _screen_size()

        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.bind((self._HOST, self._PORT))

    def start(self):
        self._server_socket.listen()
        conn_socket, addr = self._server_socket.accept()

        self._receive(conn_socket, addr)

    def _receive(self, conn_socket: socket.socket, addr: (str, int)):
        """Receive data from client

        1. receive data from client
        2. unpacking & unpickling received data
        3. show client screen with cv2.imshow()

        Args:
            conn_socket: socket.socket
                connected client socket
            addr: (str, int)
                connected client address
        """
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

                width, height, payload_size = \
                    struct.unpack('>III', packed_payload_size)

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
                    screen = cv2.resize(screen,
                                        (self._WIDTH, self._HEIGHT),
                                        interpolation=cv2.INTER_AREA)

                cv2.imshow(winname=str(addr), mat=screen)
                if cv2.waitKey(1) == 27:
                    raise StopIteration
        except StopIteration:
            conn_socket.close()
            cv2.destroyWindow(winname=str(addr))
            print('Mirroring ends...')
