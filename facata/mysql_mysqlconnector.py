from facata.utils import Connection, to_pyformat


class MysqlMysqlConnectConnection(Connection):
    def run(self, sql, **params):
        self.cur.execute(to_pyformat(sql), params)
        return None if self.cur.description is None else self.cur.fetchall()

    @property
    def notifications(self):
        return []

    @property
    def parameter_statuses(self):
        return []


def connect(dbname, user, password, host, port, params):
    import mysql.connector

    for param, paramname in ((port, "port"),):
        if param is not None:
            params[paramname] = param

        if "autocommit" not in params:
            params["autocommit"] = True

    c = mysql.connector.connect(user=user, password=password, database=dbname, **params)
    return MysqlMysqlConnectConnection(c)
