from datetime import timedelta as Timedelta
import pg8000.native
import pytest
from facata import connect


def test_connect_live(postgresql_host):
    con = connect(
        "postgresql",
        "pg8000",
        user="postgres",
        password="pw",
        host=postgresql_host,
    )
    result = con.run("SELECT 'Hello'")
    con.close()

    assert result == [["Hello"]]


@pytest.mark.parametrize(
    "params",
    [
        {"user": "postgres"},
        {"user": "postgres", "password": "pw"},
    ],
)
def test_connect(params, mocker):
    def init(
        self,
        user,
        host="localhost",
        database=None,
        port=5432,
        password=None,
        source_address=None,
        unix_sock=None,
        ssl_context=None,
        timeout=None,
        tcp_keepalive=True,
        application_name=None,
        replication=None,
    ):
        assert password == params.get("password")

    mocker.patch.object(pg8000.native.Connection, "__init__", init)
    connect("postgresql", "pg8000", **params)


def test_register_py_to_db(postgresql_pg8000_con):
    class MyInterval(str):
        pass

    def my_interval_py_to_db(my_interval):
        return my_interval  # Must return a str

    postgresql_pg8000_con.register_py_to_db(MyInterval, 1186, my_interval_py_to_db)
    result = postgresql_pg8000_con.run(
        "SELECT :interval", interval=MyInterval("2 hours")
    )
    assert result == [[Timedelta(seconds=7200)]]
