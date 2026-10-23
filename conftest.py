import pymysql
import pytest

def pytest_addoption(parser):
    parser.addoption("--host", action="store", default="localhost")
    parser.addoption("--port", action="store", default=3306, type=int)
    parser.addoption("--database", action="store", default="prestashop")
    parser.addoption("--user", action="store", default="root")
    parser.addoption("--password", action="store", default="admin")

@pytest.fixture(scope="session")
def connection(request):
    connection = pymysql.connect(
        host=request.config.getoption("--host"),
        port=request.config.getoption("--port"),
        database=request.config.getoption("--database"),
        user=request.config.getoption("--user"),
        password=request.config.getoption("--password"),
        charset="utf8mb4",
    )

    try:
        yield connection
    finally:
        connection.close()