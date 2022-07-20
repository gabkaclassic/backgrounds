from configuration import Configuration, update_config, save_config
from time import strptime, sleep
from process import Handler
from whallpaper_chooser import set_wallpaper

import win10toast, platform, os

FORMAT_TIME = "%H:%M:%S"


def check_directory():
    update_config()
    handler = Handler(Configuration.CONFIG)
    handler.process_directory()
    set_wallpaper(handler)
    save_config(handler.count)


def notify(exception):

    message = f"Running of application was finished with error: {exception}"
    title = "Backgrounds"
    plt = platform.system()
    if plt == "Darwin":
        command = '''
        osascript -e 'display notification "{message}" with title "{title}"'
        '''
    elif plt == "Linux":
        command = f'''
        notify-send "{title}" "{message}"
        '''
    elif plt == "Windows":
        win10toast.ToastNotifier().show_toast(title, message)
        return
    else:
        return
    os.system(command)


def start():
    try:
        while True:
            check_directory()
            time = strptime(Configuration.CONFIG['sleep_time'], FORMAT_TIME)
            seconds = (time.tm_hour * 60 ** 2) + (time.tm_min * 60) + time.tm_sec
            sleep(seconds)
    except Exception as exception:
        notify(exception)
    finally:
        exit(0)


if __name__ == '__main__':
    start()
