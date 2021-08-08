import sqlite3
from facata import connect
from facata.sqlite_sqlite3 import SqliteSqlite3Connection


def listize(a):
    b = list(a) if isinstance(a, tuple) else a

    return [listize(c) for c in b] if isinstance(b, list) else b


def test_connection_context_manager(con_arg):
    dbms, driver, kwargs = con_arg
    with connect(dbms, driver, **kwargs) as con:
        result = con.run("SELECT 'Hello'")
    assert listize(result) == [["Hello"]]


def test_parameters(con):
    value = "Hello"
    result = con.run("SELECT :value", value=value)
    assert listize(result) == [[value]]


def test_column_metadata(con):
    con.run("SELECT 'Blue' as colour")
    assert con.columns[0]["name"] == "colour"


def test_connection_property(con):
    con.connection


def start_transaction(con):
    if isinstance(con, SqliteSqlite3Connection):
        return "BEGIN"  # SQLite doesn't understand START TRANSACTION
    else:
        return "START TRANSACTION"


def test_autocommit(con):
    con.run(start_transaction(con))
    con.run("SELECT 'Hello'")
    con.run("COMMIT")


def test_prepare(con):
    ps = con.prepare("SELECT 'Hello'")
    result = ps.run()
    assert listize(result) == [["Hello"]]


def test_prepare_params(con):
    v = 0
    ps = con.prepare("SELECT CAST(:v AS FLOAT)")
    result = ps.run(v=v)
    assert listize(result) == [[v]]


def test_transaction(con):
    con.run("CREATE TEMPORARY TABLE book (id SERIAL, title TEXT)")
    try:
        con.run("ROLLBACK")
    except sqlite3.OperationalError:
        pass
    result = con.run("SELECT * FROM book")
    assert listize(result) == []
