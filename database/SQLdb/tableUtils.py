from database import getConnection

def addToTable(name: str, settings: dict) -> None:
    conn = getConnection()
    keys: str = ''
    values: str = ''
    for key, value in settings.items():
        keys += f'{key},'
        if type(value) is str:
            values += f'\'{value}\','
        else: 
            values += f'{value},'
    with conn.cursor() as cur:
        cur.execute(f'INSERT INTO {name} ({keys[:-1]})\
                    VALUES ({values[:-1]})\
                    ON CONFLICT DO NOTHING;')
    conn.commit()
    conn.close()

def updateFromTable(name: str, id: dict, settings: dict) -> None:
    conn = getConnection()
    setters: str = ''
    for key, value in settings.items():
        setters += f'{key} = \'{value}\', '
    with conn.cursor() as cur:
        cur.execute(f'UPDATE {name}\
                    SET {setters[:-2]}\
                    WHERE {list(id.keys())[0]} = {list(id.values())[0]};')
    conn.commit()
    conn.close()

def deleteFromTable(name: str, key: str, value: str) -> None:
    conn = getConnection()
    if type(value) is str:
        value = f'\'{value}\''
    with conn.cursor() as cur:
        cur.execute(f'DELETE FROM {name}\
                    WHERE {key} = {value};')
    conn.commit()
    conn.close()

def clearTable(name: str) -> None:
    conn = getConnection()
    with conn.cursor() as cur:
        cur.execute(f'DELETE FROM {name};')
    conn.commit()
    conn.close()

def getFromTable(name: str, condition: str = '') -> tuple:
    conn = getConnection()
    with conn.cursor() as cur:
        cur.execute(f'SELECT * FROM {name}\
                    {condition};')
        return cur.fetchall()