import pytest
from starlette_app import models


@pytest.mark.asyncio
async def test_signup_user_successful(client, database):
    async with database:
        assert await models.User.objects.count() == 0
        response = await client.post(
            "/signup",
            data={
                "full_name": "Danny Devito",
                "email": "danny@example.com",
                "password": "password1010",
                "confirm_password": "password1010",
            }
        )
        assert await models.User.objects.count() == 1
        user = await models.User.objects.first()
        assert user.full_name == "Danny Devito"
        assert user.email == "danny@example.com"
        assert user.check_password("password1010")
        
        assert "/user" in str(response.url)

@pytest.mark.asyncio
async def test_login_user_successfully(client, database):
    assert await models.User.objects.count() == 1
    
    response = await client.post(
        "/login", data={"email": "danny@example.com", "password": "password"}
    )
    import pdb; pdb.set_trace()
    assert response == 302
    
    # assert "/user" in response.headers["Location"]
    
    
def test_only_logged_in_user_in_user_page(client, create_user,Login):
    response =await client.get("/user")
    assert await models.User.query.count() == 1
    assert response.status_code == 302
    assert "/login?next=%2Fuser" in response.headers["Location"]
    assert User.username == 
    response = client.get("/user")
    
    assert response.status_code == 302 
    # assert "User Dashboard".encode('utf-8') in response.content