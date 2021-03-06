from facata import connect


def test_connect(mariadb_host):
    con = connect(
        "mariadb",
        "mariadb",
        username="root",
        password="pw",
        host=mariadb_host,
        port=3306,
    )
    result = con.run("SELECT 'Hello'")
    con.close()

    assert result == [("Hello",)]
