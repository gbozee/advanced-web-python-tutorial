import pytest
from flask_app import app


@pytest.fixture
def client():
    # db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
    app.config["TESTING"] = True

    with app.test_client() as client:
        # with app.app_context():
        #     flaskr.init_db()
        yield client

    # os.close(db_fd)
    # os.unlink(flaskr.app.config['DATABASE'])


def test_home_page(client):
    response = client.get("/")
    assert response.data.decode('utf-8') == "Hello world"

