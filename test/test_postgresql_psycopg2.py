import pytest
from facata import connect


def test_connect_live(postgresql_host):
    con = connect(
        "postgresql",
        "psycopg2",
        host=postgresql_host,
        username="postgres",
        password="pw",
    )
    result = con.run("SELECT 'Hello'")
    con.close()

    assert result == [("Hello",)]


@pytest.mark.parametrize(
    "params,expected",
    [
        [
            {"username": "postgres"},
            {"user": "postgres", "dbname": None, "password": None},
        ],
        [
            {"username": "postgres", "password": "pw"},
            {"user": "postgres", "password": "pw", "dbname": None},
        ],
        [
            {"username": "postgres", "host": "localhost"},
            {"user": "postgres", "host": "localhost", "dbname": None, "password": None},
        ],
    ],
)
def test_connect(params, expected, mocker):
    mock_connect = mocker.patch("psycopg2.connect")
    connect("postgresql", "psycopg2", **params)
    mock_connect.assert_called_with(**expected)
