""" Sample Client """

import threading

from ssm import ScreenMirrorClient


client = ScreenMirrorClient('localhost', quality=90, cursor=True)

t = threading.Thread(target=client.start)
t.start()

