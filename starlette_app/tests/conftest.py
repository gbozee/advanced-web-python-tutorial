import pytest
import httpx
import os
from starlette.testclient import TestClient
import sqlalchemy
from starlette_app.app import app, models
import databases

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_LOCATION = os.path.join(BASE_DIR, "test.db")

TEST_DB = "sqlite:///{}".format(DB_LOCATION)


@pytest.fixture
def client():
    return httpx.Client(app=app, base_url="http://test_server")
    # return httpx.Client(app=app,base_url="http://test_server")
    # return TestClient(app, raise_server_exceptions=True)


@pytest.fixture(scope="session")
def metadata(database):
    metadata = models.init_tables(database)
    return metadata


@pytest.fixture(scope="session")
def database():
    return databases.Database(TEST_DB)


@pytest.fixture(autouse=True, scope="session")
def create_test_database(metadata):
    engine = sqlalchemy.create_engine(TEST_DB)
    metadata.create_all(engine)
    # config = Config("alembic.ini")   # Run the migrations.
    # command.upgrade(config, "head")
    yield
    # command.downgrade(config, "head")                  # Run the tests.
    metadata.drop_all(engine)
