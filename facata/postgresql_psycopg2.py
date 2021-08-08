from facata.utils import Connection, to_pyformat


class PostgresqlPsycopg2Connection(Connection):
    def run(self, sql, **params):
        self.cur.execute(to_pyformat(sql), params)
        return None if self.cur.description is None else self.cur.fetchall()

    @property
    def notifications(self):
        return self.con.notices

    @property
    def parameter_statuses(self):
        return []

    def register_py_to_db(self, cls, type_code, adapter):
        from psycopg2.extensions import register_adapter

        register_adapter(cls, adapter)

    def register_db_to_py(self, type_code, adapter):
        from psycopg2.extensions import new_type, register_type

        TYP = new_type((type_code,), str(type_code), adapter)
        register_type(TYP)


def connect(dbname, username, password, host, port, params):
    import psycopg2

    if host is not None:
        params["host"] = host
    if port is not None:
        params["port"] = port

    con = psycopg2.connect(dbname=dbname, user=username, password=password, **params)
    con.autocommit = True

    return PostgresqlPsycopg2Connection(con)
