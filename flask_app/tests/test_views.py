from flask_app import models
import pytest
from flask_app.models import User



# def test_home_page(client):
#     response = client.get("/")
#     assert response.data.decode("utf-8") == "Hello world"

@pytest.fixture
def create_user():
    # create sample user

    user_1 = User(
        email="danny@example.com",
        full_name="Danny Devito",
    )
    user_1.set_password("password")
    user_1.save()
    return user_1

@pytest.fixture
def Login():
    # create sample user

    user = User(
        email="danny@example.com",
        password="passwordd",
    )
    return user

def test_signup_user_successful(client):
    assert models.User.query.count() == 0
    response = client.post(
        "/signup",
        data={
            "full_name": "Danny Devito",
            "email": "danny@example.com",
            "password": "password1010",
            "confirm_password": "password1010",
        },
    )
    assert models.User.query.count() == 1
    user = models.User.query.first()
    assert user.full_name == "Danny Devito"
    assert user.email == "danny@example.com"
    assert user.check_password("password1010")

    assert response.status_code == 302
    # assert "/user" in response.headers["Location"]



def test_login_user_successfully(client, create_user):
    assert models.User.query.count() == 1
    response = client.post(
        "/login", data={"email": "danny@example.com", "password": "password"}
    )
    assert response.status_code == 302
    assert "/user" in response.headers["Location"]
    
    
    
def test_only_logged_in_user_in_user_page(client, create_user,Login):
    response = client.get("/user")
    assert models.User.query.count() == 1
    assert response.status_code == 302
    assert "/login?next=%2Fuser" in response.headers["Location"]
    assert User.username == 
    response = client.get("/user")
    
    assert response.status_code == 302 
    # assert "User Dashboard".encode('utf-8') in response.content