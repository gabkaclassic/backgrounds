import json


def save_config(count):
    Configuration.CONFIG.update({'count': count})
    with open(Configuration.CONFIGURATION_FILENAME, 'w') as f:
        json.dump(Configuration.CONFIG, f)


def update_config():
    with open(Configuration.CONFIGURATION_FILENAME, 'r') as f:
        Configuration.CONFIG = json.loads(f.read())


class Configuration:
    CONFIGURATION_FILENAME = "config.json"
    CONFIG = dict()
