""" TEST CLIENT """

import sys
import threading

from ssm import client


client = client.ScreenMirrorClient('localhost')
#client = client.ScreenMirrorClient('msi-private')

t = threading.Thread(target=client.start)
t.start()

key = ord(input("")) & 0xFF
while key != 27:
    pass

sys.exit()

