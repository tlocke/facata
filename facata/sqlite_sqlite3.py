from facata.utils import Connection


class SqliteSqlite3Connection(Connection):
    def run(self, sql, **params):
        self.cur = self.con.execute(sql, params)
        return None if self.cur.description is None else self.cur.fetchall()

    def register_py_to_db(self, cls, type_code, adapter):
        self.module.register_adapter(cls, adapter)

    def register_db_to_py(self, type_code, adapter):
        self.module.register_converter(type_code, adapter)

    @property
    def notifications(self):
        return []

    @property
    def paramster_statuses(self):
        return []


def connect(dbname, username, password, host, port, params):
    import sqlite3

    if "isolation_level" not in params:
        params["isolation_level"] = None  # Don't override SQLite's autocommit

    c = sqlite3.connect(dbname, **params)
    return SqliteSqlite3Connection(c, module=sqlite3)
