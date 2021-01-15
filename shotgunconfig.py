import configparser


class ShotgunConfig:
    def __init__(self, path):
        c = configparser.ConfigParser()
        c.read(path)
        for item in c['general']['list'].split(','):
            category = item.split(':')[0]
            var = item.split(':')[1]
            setattr(self, var, c[category][var])
        for category in c.sections():
            for item in c[category]:
                if str(category)+':'+str(item) not in c['general']['list'] and item != 'list':
                    setattr(self, item, c[category][item])
