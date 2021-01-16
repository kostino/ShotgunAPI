import configparser


class ShotgunConfig:
    def __init__(self, path):
        c = configparser.ConfigParser()
        c.read(path)
        for item in c['general']['list'].split(','):
            print(item)
            category = item.split(':')[0]
            var = item.split(':')[1]
            print(category)
            print(var)
            setattr(self, var, c[category][var].split(','))
        for category in c.sections():
            for item in c[category]:
                if str(category)+':'+str(item) not in c['general']['list'] and item != 'list':
                    setattr(self, item, c[category][item])
