from database import getConnection

def createTable(name: str, settings: dict) -> None:
    conn = getConnection()
    values: str = ''
    for key, value in settings.items():
        values += f'{key} {value},'
    with conn.cursor() as cur:
        cur.execute(f'CREATE TABLE IF NOT EXISTS {name} ({values[:-1]});')
    conn.commit()
    conn.close()

def deleteTable(name: str) -> None:
    conn = getConnection()
    with conn.cursor() as cur:
        cur.execute(f'DROP TABLE IF EXISTS {name};')
    conn.commit()
    conn.close()

def loadTables() -> None:
    createTable('moder', {'username': 'VARCHAR(255)'})
    createTable('orders', {'username': 'VARCHAR(255)',
                           'product': 'VARCHAR(255)'})
    createTable('utils', {'id': 'BIGINT PRIMARY KEY',
                          'username': 'VARCHAR(255)',
                          'position': 'VARCHAR(255)',
                          'toAdd': 'VARCHAR(255)',
                          'toDelete': 'VARCHAR(255)'})