from psycopg2 import connect
from psycopg2.extensions import connection, cursor
from config import Config, loadConfig

def getConnection() -> connection:
    config: Config = loadConfig()
    return connect(host=config.db.host,
                   port=config.db.port,
                   dbname=config.db.name,
                   user=config.db.user,
                   password=config.db.password)

def getCursor() -> cursor:
    return getConnection().cursor()