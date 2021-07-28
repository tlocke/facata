from facata.utils import Connection, to_pyformat


class PostgresqlPsycopg2Connection(Connection):
    def __init__(self, con):
        super().__init__(con)

    def run(self, sql, **params):
        cur = self.con.cursor()

        psql = to_pyformat(sql)

        cur.execute(psql, params)
        return cur.fetchall()


def connect(dbname, username, password, host, port, params):
    import psycopg2

    if host is not None:
        params["host"] = host
    if port is not None:
        params["port"] = port

    con = psycopg2.connect(dbname=dbname, user=username, password=password, **params)

    return PostgresqlPsycopg2Connection(con)
