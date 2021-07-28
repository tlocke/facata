from facata.utils import Connection, to_pyformat


class MariadbMariadbConnection(Connection):
    def __init__(self, con):
        super().__init__(con)

    def run(self, sql, **params):
        cur = self.con.cursor()

        psql = to_pyformat(sql)

        cur.execute(psql, params)
        return cur.fetchall()


def connect(dbname, username, password, host, port, params):
    import mariadb

    for param, paramname in ((dbname, "database"), (port, "port")):
        if param is not None:
            params[paramname] = param

    c = mariadb.connect(host=host, user=username, password=password, **params)
    return MariadbMariadbConnection(c)
