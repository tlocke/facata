import pytest

from facata import connect


@pytest.mark.parametrize(
    "params",
    [
        {"user": "root"},
        {"user": "root", "host": "mysqldb"},
    ],
)
def test_connect(params, mocker):
    mock_connect = mocker.patch("mysql.connector.connect")
    connect("mysql", "mysql-connector", **params)
    expected = {"password": None, "database": None, "autocommit": True}
    expected.update(params)
    mock_connect.assert_called_with(**expected)
