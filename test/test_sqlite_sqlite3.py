import sqlite3
from decimal import Decimal
from facata import connect


def test_connect():
    con = connect("sqlite", "sqlite3", dbname=":memory:")
    result = con.run("SELECT 'Hello'")
    con.close()

    assert result == [("Hello",)]


def test_register_py_to_db():
    con = connect("sqlite", "sqlite3", dbname=":memory:")

    def decimal_py_to_db(dec):
        return str(dec)

    val = Decimal("0.1")
    con.register_py_to_db(Decimal, None, decimal_py_to_db)
    result = con.run("SELECT :val", val=val)
    assert result == [(str(val),)]


def test_register_db_to_py():
    con = connect(
        "sqlite", "sqlite3", dbname=":memory:", detect_types=sqlite3.PARSE_DECLTYPES
    )

    def decimal_db_to_py(data):
        return Decimal(data.decode("ascii"))

    con.register_db_to_py("decimal", decimal_db_to_py)

    con.run("CREATE TEMPORARY TABLE book (price decimal)")
    con.run("INSERT INTO book (price) VALUES (:price)", price="7.99")
    result = con.run("SELECT * FROM book")
    assert result == [(Decimal("7.99"),)]
