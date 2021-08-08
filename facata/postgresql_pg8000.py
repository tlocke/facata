from facata.utils import Connection, PreparedStatement


class PostgresqlPg8000Connection(Connection):
    def __init__(self, con, module=None):
        self.con = con

    def run(self, sql, **params):
        return self.con.run(sql, **params)

    @property
    def columns(self):
        return self.con.columns

    def close(self):
        self.con.close()

    @property
    def notifications(self):
        return self.con.notifications

    @property
    def parameter_statuses(self):
        return self.con.parameter_statuses

    def register_py_to_db(self, cls, type_code, adapter):
        self.con.register_out_adapter(cls, type_code, adapter)

    def register_db_to_py(self, type_code, adapter):
        self.con.register_in_adapter(type_code, adapter)

    def prepare(self, sql):
        return PreparedStatement(self.con.prepare(sql))


def connect(dbname, user, password, host, port, params):
    import pg8000.native

    for param, paramname in ((host, "host"), (port, "port")):
        if param is not None:
            params[paramname] = param

    c = pg8000.native.Connection(user, database=dbname, password=password, **params)
    return PostgresqlPg8000Connection(c)
