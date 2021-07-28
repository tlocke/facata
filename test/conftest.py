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
        "--postgresql-host",
        action="store",
        default="localhost",
        help="Hostname of PostgreSQL",
    )


@pytest.fixture
def mariadb_host(request):
    return request.config.getoption("--mariadb-host")


@pytest.fixture
def postgresql_host(request):
    return request.config.getoption("--postgresql-host")


CONNECT_ARGS = {
    "mariadb": {
        "mariadb": {
            "username": "root",
            "password": "pw",
            "port": 3306,
        },
    },
    "postgresql": {
        "pg8000": {"username": "postgres", "password": "pw"},
        "psycopg2": {"username": "postgres", "password": "pw", "host": "localhost"},
    },
    "sqlite": {
        "sqlite3": {},
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

    if dbms in ("mariadb", "postgresql"):
        kwargs["host"] = request.config.getoption(f"--{dbms}-host")

    yield dbms, driver, kwargs


@pytest.fixture(params=con_args)
def con(request):
    dbms, driver, kwargs = request.param
    c = connect(dbms, driver, **kwargs)
    yield c
    c.close()
