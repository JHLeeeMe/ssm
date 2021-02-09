""" TEST CLIENT """

import sys
import threading

from ssm import client


#client = client.ScreenMirrorClient('msi-private', cursor=True)
client = client.ScreenMirrorClient('localhost')

t = threading.Thread(target=client.start)
t.start()

key = ord(input("")) & 0xFF
while key != 27:
    pass

sys.exit()

