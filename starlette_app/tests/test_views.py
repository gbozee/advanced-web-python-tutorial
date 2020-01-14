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
