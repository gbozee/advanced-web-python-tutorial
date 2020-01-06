
import pytest
import httpx
from starlette_app import app
from starlette.testclient import TestClient

@pytest.fixture 
def client():
    # return httpx.Client(app=app)
    return TestClient(app)


def test_home_page(client):
    response = client.get("/")
    assert response.text == 'Hello world'