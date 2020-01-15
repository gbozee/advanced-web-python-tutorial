import pytest
from django.contrib.auth.models import User
from django.test import SimpleTestCase
from django.db import IntegrityError
# from django.db.models.sql.


@pytest.fixture
def create_user():
    # create sample user

    user_1 = User.objects.create(
        username="danny@example.com",
        email="danny@example.com",
        first_name="Danny Devito",
    )
    user_1.set_password("password")
    user_1.save()
    return user_1


@pytest.mark.django_db
def test_signup_user_successful(client):
    assert User.objects.count() == 0
    response = client.post(
        "/signup",
        data={
            "full_name": "Danny Devito",
            "email": "danny@example.com",
            "password": "password1010",
            "confirm_password": "password1010",
        },
    )
    assert response.status_code == 302
    assert response.url == "/user"
    assert User.objects.count() == 1
    user = User.objects.first()
    assert user.first_name == "Danny Devito"
    assert user.username == "danny@example.com"
    assert user.email == "danny@example.com"
    assert user.check_password("password1010")
    # assert response.content.decode("utf-8") == "Hello world"


@pytest.mark.django_db
def test_login_user_successfully(client, create_user):
    assert User.objects.count() == 1
    response = client.post(
        "/login", data={"email": "danny@example.com", "password": "password"}
    )
    assert response.status_code == 302
    assert response.url == "/user"


@pytest.mark.django_db
def test_only_logged_in_user_in_user_page(client, create_user):
    response = client.get("/user")
    assert response.status_code == 302
    assert response.url == "/login?next=/user"
    client.login(username="danny@example.com", password="password")
    response = client.get("/user")
    assert response.status_code == 200 
    assert "User Dashboard".encode('utf-8') in response.content

@pytest.mark.django_db
def test_user_already_exist(client,create_user):
     response = client.post(
         "/signup",
         data={
             "full_name": "James Devito",
             "email": "james@example.com",
             "password": "password1010",
             "confirm_password": "password1010",
             },
    )
    #  import pdb; pdb.set_trace()
     assert response.status_code == 200
     assert User.objects.count() == 1

     assert User.objects.filter(username='danny@example.com') != 'james@example.com'
    #  assert user.username == "danny@example.com" 
    #  user= User.objects.filter(user)

     
     
