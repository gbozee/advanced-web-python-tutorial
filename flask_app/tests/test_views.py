from flask_app import models


def test_home_page(client):
    response = client.get("/")
    assert response.data.decode("utf-8") == "Hello world"


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
    assert "/user" in response.headers["Location"]
