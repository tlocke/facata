from facata.utils import Connection


def connect(dbname, username, password, host, port, params):
    import sqlite3

    if dbname is None:
        dbname = ":memory:"

    c = sqlite3.connect(dbname, **params)
    return Connection(c)
