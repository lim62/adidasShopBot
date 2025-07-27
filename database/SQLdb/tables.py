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

def loadTables() -> None:
    createTable('moder', {'username': 'VARCHAR(255)'})
    createTable('categories', {'name': 'VARCHAR(255)',
                               'position': 'VARCHAR(255)'})
    createTable('products', {'name': 'VARCHAR(255)',
                             'description': 'VARCHAR(255)',
                             'price': 'VARCHAR(255)',
                             'photo': 'VARCHAR(255)',
                             'position': 'VARCHAR(255)'})
    createTable('orders', {'username': 'VARCHAR(255)',
                           'product': 'VARCHAR(255)'})
    createTable('utils', {'id': 'BIGINT PRIMARY KEY',
                          'username': 'VARCHAR(255)',
                          'position': 'VARCHAR(255)',
                          'toAdd': 'VARCHAR(255)',
                          'toDelete': 'VARCHAR(255)'})