import pytest

from facata import connect
from facata.core import CONNECT_FUNCS


def pytest_addoption(parser):
    parser.addoption(
        "--mariadb-host",
        action="store",
        default="127.0.0.1",
        help="Hostname of MariaDB",
    )

    parser.addoption(
        "--mysql-host",
        action="store",
        default="127.0.0.1",
        help="Hostname of MySQL",
    )

    parser.addoption(
        "--postgresql-host",
        action="store",
        default="localhost",
        help="Hostname of PostgreSQL",
    )


@pytest.fixture
def mariadb_host(request):
    return request.config.getoption("--mariadb-host")


@pytest.fixture
def mysql_host(request):
    return request.config.getoption("--mysql-host")


@pytest.fixture
def postgresql_host(request):
    return request.config.getoption("--postgresql-host")


CONNECT_ARGS = {
    "mariadb": {
        "mariadb": {
            "user": "root",
            "password": "pw",
            "dbname": "mysql",
            "port": 3306,
        },
    },
    "mysql": {
        "mysql-connector": {
            "user": "root",
            "password": "pw",
            "dbname": "mysql",
            "port": 3305,
        },
    },
    "postgresql": {
        "pg8000": {"user": "postgres", "password": "pw"},
        "psycopg2": {"user": "postgres", "password": "pw", "host": "localhost"},
    },
    "sqlite": {
        "sqlite3": {"dbname": ":memory:"},
    },
}


con_args = []
for dbms, drivers in CONNECT_FUNCS.items():
    dbms_args = CONNECT_ARGS[dbms]
    for driver in drivers.keys():
        args = (dbms, driver, dbms_args[driver])
        con_args.append(pytest.param(args, id=f"{dbms}-{driver}"))


@pytest.fixture(params=con_args)
def con_arg(request):
    dbms, driver, kwargs = request.param

    if dbms in ("mariadb", "mysql", "postgresql"):
        kwargs["host"] = request.config.getoption(f"--{dbms}-host")

    yield dbms, driver, kwargs


@pytest.fixture(params=con_args)
def con(request):
    dbms, driver, kwargs = request.param
    c = connect(dbms, driver, **kwargs)
    yield c
    c.close()


@pytest.fixture()
def postgresql_pg8000_args(request):
    kwargs = CONNECT_ARGS["postgresql"]["pg8000"]

    kwargs["host"] = request.config.getoption("--postgresql-host")

    yield kwargs


@pytest.fixture()
def postgresql_pg8000_con(postgresql_pg8000_args):
    con = connect("postgresql", "pg8000", **postgresql_pg8000_args)
    yield con
    con.close()


@pytest.fixture()
def postgresql_psycopg2_args(request):
    kwargs = CONNECT_ARGS["postgresql"]["psycopg2"]

    kwargs["host"] = request.config.getoption("--postgresql-host")

    yield kwargs


@pytest.fixture()
def postgresql_psycopg2_con(postgresql_psycopg2_args):
    con = connect("postgresql", "psycopg2", **postgresql_psycopg2_args)
    yield con
    con.close()
