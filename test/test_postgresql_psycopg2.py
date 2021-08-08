import re
from psycopg2.extensions import AsIs
import pytest
from facata import connect


def test_connect_live(postgresql_host):
    con = connect(
        "postgresql",
        "psycopg2",
        host=postgresql_host,
        user="postgres",
        password="pw",
    )
    result = con.run("SELECT 'Hello'")
    con.close()

    assert result == [("Hello",)]


@pytest.mark.parametrize(
    "params,expected",
    [
        [
            {"user": "postgres"},
            {"user": "postgres", "dbname": None, "password": None},
        ],
        [
            {"user": "postgres", "password": "pw"},
            {"user": "postgres", "password": "pw", "dbname": None},
        ],
        [
            {"user": "postgres", "host": "localhost"},
            {"user": "postgres", "host": "localhost", "dbname": None, "password": None},
        ],
    ],
)
def test_connect(params, expected, mocker):
    mock_connect = mocker.patch("psycopg2.connect")
    connect("postgresql", "psycopg2", **params)
    mock_connect.assert_called_with(**expected)


def test_register_py_to_db(postgresql_psycopg2_con):
    class Point(object):
        def __init__(self, x, y):
            self.x = x
            self.y = y

    def point_py_to_db(point):
        return AsIs("'(%s, %s)'" % (point.x, point.y))

    postgresql_psycopg2_con.register_py_to_db(Point, None, point_py_to_db)
    result = postgresql_psycopg2_con.run("SELECT cast(:pt as point)", pt=Point(2, 4))
    assert result == [("(2,4)",)]


def test_register_db_to_py(postgresql_psycopg2_con):
    class Point(object):
        def __init__(self, x, y):
            self.x = x
            self.y = y

        def __eq__(self, other):
            return isinstance(other, Point) and self.x, self.y == other.x, other.y

    def point_db_to_py(value, cur):
        if value is None:
            return None

        m = re.match(r"\(([^)]+),([^)]+)\)", value)
        return Point(float(m.group(1)), float(m.group(2)))

    postgresql_psycopg2_con.register_db_to_py(600, point_db_to_py)
    result = postgresql_psycopg2_con.run("SELECT cast('(2,4)' as point)")
    assert result == [(Point(2, 4),)]


def test_lo(postgresql_psycopg2_con):

    data = b"hello"
    res = postgresql_psycopg2_con.run("SELECT lo_from_bytea(0, :data)", data=data)
    oid = res[0][0]

    postgresql_psycopg2_con.run("CREATE TEMPORARY TABLE image (raster oid)")
    postgresql_psycopg2_con.run("INSERT INTO image (raster) VALUES (:oid)", oid=oid)

    result = postgresql_psycopg2_con.run("SELECT lo_get(:oid)", oid=oid)
    assert bytes(result[0][0]) == b"hello"
