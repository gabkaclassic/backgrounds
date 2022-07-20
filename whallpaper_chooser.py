import ctypes
from random import randint as rand


def set_wallpaper(handler):
    filename = handler.download_file(rand(0, handler.count))
    ctypes.windll.user32.SystemParametersInfoW(20, 0, filename, 0)

