import facata.mariadb_mariadb
import facata.mysql_mysqlconnector
import facata.postgresql_pg8000
import facata.postgresql_psycopg2
import facata.sqlite_sqlite3
from facata.exceptions import FacataException


CONNECT_FUNCS = {
    "mariadb": {
        "mariadb": facata.mariadb_mariadb.connect,
    },
    "mysql": {
        "mysql-connector": facata.mysql_mysqlconnector.connect,
    },
    "postgresql": {
        "pg8000": facata.postgresql_pg8000.connect,
        "psycopg2": facata.postgresql_psycopg2.connect,
    },
    "sqlite": {
        "sqlite3": facata.sqlite_sqlite3.connect,
    },
}


def connect(
    dbms,
    driver,
    dbname=None,
    user=None,
    password=None,
    host=None,
    port=None,
    **params,
):

    try:
        dbms_connects = CONNECT_FUNCS[dbms]
    except KeyError as e:
        raise FacataException(
            f"The dbms must be one of {list(CONNECT_FUNCS.keys())}, but the specified "
            f"dbms was {e}"
        )

    try:
        connect_f = dbms_connects[driver]
    except KeyError as e:
        raise FacataException(
            f"The driver must be one of {list(dbms_connects.keys())}, but the "
            f"specified driver was {e}"
        )
    return connect_f(dbname, user, password, host, port, params)
