import pytest
import os
from flask_app import create_app, models, db

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_LOCATION = os.path.join(BASE_DIR, "test.db")

TEST_DB = "sqlite:///{}".format(DB_LOCATION)


@pytest.fixture
def app():
    _app = create_app(TEST_DB)
    return _app


@pytest.fixture
def client(app):
    # db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
    app.config["TESTING"] = True

    with app.test_client() as client:
        with app.app_context():
            db.drop_all()
            db.create_all()
            yield client

    # os.close(db_fd)
    # os.unlink(flaskr.app.config['DATABASE'])
