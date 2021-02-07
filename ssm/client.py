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
        self._host = host
        self._port = port
        self._quality = quality
        self._cursor = cursor
        self._client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        t = threading.Thread(target=self._send)
        t.start()
        t.join()

    def _send(self):
        self._client_socket.connect((self._host, self._port))
        while True:
            try:
                data = self._get_screen()
                encoded_data = self._encode(data)
                b_encoded_data = pickle.dumps(encoded_data)
                b_encoded_data_size = len(b_encoded_data)

                self._client_socket.sendall(
                    struct.pack('>I', b_encoded_data_size) + b_encoded_data
                )
            except Exception as e:
                print(e)
                break

    def _get_screen(self) -> np.ndarray:
        screen = np.array(ImageGrab.grab())
        if self._cursor:
            screen = cv2.circle(screen, self._mouse_position(), 5, (0, 0, 255), -1)

        cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)
        return screen

    def _mouse_position(self) -> (int, int):
        display = Display(os.environ['DISPLAY'])
        coordinates = display.screen().root.query_pointer()._data
        return coordinates['root_x'], coordinates['root_y']

    def _encode(self, data) -> np.ndarray:
        encode_param = (cv2.IMWRITE_JPEG_QUALITY, self._quality)
        _, encoded_data = cv2.imencode('.jpg', data, params=encode_param)
        return encoded_data
