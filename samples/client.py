""" Sample Client """

from ssm import ScreenMirrorClient


client = ScreenMirrorClient('localhost', quality=90, cursor=True)
client.start()

