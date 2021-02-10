"""client
"""

import os
import struct
import pickle
import socket
import threading

import cv2
import numpy as np
from PIL import ImageGrab
from Xlib.display import Display


class ScreenMirrorClient:
    def __init__(self, host: str, port: int = 7890, quality: int = 80, cursor: bool = False):
        self._HOST = host
        self._PORT = port

        self._QUALITY = quality
        self._CURSOR = cursor

        self._client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        t = threading.Thread(target=self._send)
        t.start()
        t.join()

    def _send(self):
        self._client_socket.connect((self._HOST, self._PORT))
        while True:
            try:
                screen = self._get_screen()
                encoded_screen = self._encode(screen)
                encoded_screen_pkl = pickle.dumps(encoded_screen)
                encoded_screen_pkl_size = len(encoded_screen_pkl)

                self._client_socket.sendall(
                    struct.pack('>I', encoded_screen_pkl_size) + encoded_screen_pkl
                )
            except Exception as e:
                print(e)
                print('Mirroring ends...')
                break

    def _get_screen(self) -> np.ndarray:
        screen = np.array(ImageGrab.grab())
        if self._CURSOR:
            screen = cv2.circle(screen, self._mouse_position(), 5, (0, 0, 255), -1)

        screen = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)
        return screen

    def _mouse_position(self) -> (int, int):
        display = Display(display=os.environ['DISPLAY'])
        coordinates = display.screen().root.query_pointer()._data
        return coordinates['root_x'], coordinates['root_y']

    def _encode(self, data) -> np.ndarray:
        encode_param = (cv2.IMWRITE_JPEG_QUALITY, self._QUALITY)
        _, encoded_data = cv2.imencode(ext='.jpg', img=data, params=encode_param)
        return encoded_data
