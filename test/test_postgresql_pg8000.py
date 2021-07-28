import pg8000.native
import pytest
from facata import connect


def test_connect_live(postgresql_host):
    con = connect(
        "postgresql",
        "pg8000",
        username="postgres",
        password="pw",
        host=postgresql_host,
    )
    result = con.run("SELECT 'Hello'")
    con.close()

    assert result == [["Hello"]]


@pytest.mark.parametrize(
    "params",
    [
        {"username": "postgres"},
        {"username": "postgres", "password": "pw"},
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
