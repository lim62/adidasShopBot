from database import getCursor

def createTable(name: str, settings: dict) -> None:
    values: str = ''
    for key, value in settings.items():
        values += f'{key} {value},'
    getCursor().execute('CREATE TABLE IF NOT EXISTS %s (%s);', (settings.keys()[0], values))

def deleteTable(name: str) -> None:
    getCursor().execute('DROP TABLE IF EXISTS %s;', name)