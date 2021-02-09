""" TEST CLIENT """

import sys
import threading

from ssm import ScreenMirrorClient


client = ScreenMirrorClient('localhost', quality=90, cursor=True)

t = threading.Thread(target=client.start)
t.start()

while True:
    key = ord(input(''))
    if key == ord('q'):
        break

sys.exit()
