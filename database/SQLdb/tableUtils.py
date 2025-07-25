from database import getCursor

def addToTable(name: str, settings: dict) -> None:
    getCursor().execute('INSERT INTO %s %s VALUES %s;', (name, settings.keys(), settings.values()))

def deleteFromTable(name: str, key: str, value: str) -> None:
    getCursor().execute('DELETE FROM %s WHERE %s = %s', (name, key, value))

def getFromTable(name: str) -> list:
    cur = getCursor()
    cur.execute('SELECT * FROM %s', name)
    return cur.fetchall()