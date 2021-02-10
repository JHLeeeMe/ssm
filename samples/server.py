""" Sample Server """

import threading

from ssm import ScreenMirrorServer


server = ScreenMirrorServer()

t = threading.Thread(target=server.start)
t.start()
t.join()

