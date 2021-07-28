from facata import connect


def listize(a):
    b = list(a) if isinstance(a, tuple) else a

    return [listize(c) for c in b] if isinstance(b, list) else b


def test_sqlite_connection():
    con = connect("sqlite", "sqlite3")
    result = con.run("SELECT 'Hello'")
    con.close()

    assert result == [("Hello",)]


def test_connection_context_manager(con_arg):
    dbms, driver, kwargs = con_arg
    with connect(dbms, driver, **kwargs) as con:
        result = con.run("SELECT 'Hello'")
    assert listize(result) == [["Hello"]]


def test_parameters(con):
    value = "Hello"
    result = con.run("SELECT :value", value=value)
    assert listize(result) == [[value]]
