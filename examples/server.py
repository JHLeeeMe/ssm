""" TEST SERVER """

import sys
import threading

from ssm import ScreenMirrorServer


server = ScreenMirrorServer('', conn_limits=2)

t = threading.Thread(target=server.start)
t.start()

while True:
    key = ord(input(''))
    if key == ord('q'):
        break

sys.exit()
