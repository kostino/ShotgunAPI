import configparser


class ShotgunConfig:
    def __init__(self, path):
        c = configparser.ConfigParser()
        c.read(path)
        self.event_types = c['event']['event_types'].split(',')
