""" TEST SERVER """

import sys
import threading

from ssm import server


server = server.ScreenMirrorServer('localhost', conn_limits=2)

t = threading.Thread(target=server.start)
t.start()

key = ord(input("")) & 0xFF
while key != 27:
    pass

sys.exit()

