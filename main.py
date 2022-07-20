from configuration import Configuration, update_config, save_config
from time import strptime, sleep
from process import Handler
from whallpaper_chooser import set_wallpaper

FORMAT_TIME = "%H:%M:%S"

def check_directory():
    update_config()
    handler = Handler(Configuration.CONFIG)
    handler.process_directory()
    set_wallpaper(handler)
    save_config(handler.count)


def start():
    while True:
        check_directory()
        time = strptime(Configuration.CONFIG['sleep_time'], FORMAT_TIME)
        seconds = (time.tm_hour * 60 ** 2) + (time.tm_min * 60) + time.tm_sec
        sleep(seconds)


if __name__ == '__main__':
    start()
