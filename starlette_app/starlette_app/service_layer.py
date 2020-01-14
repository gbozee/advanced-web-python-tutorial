from pydantic import BaseModel, EmailStr, SecretStr, validator, ValidationError
from starlette_app import models


# class Login(BaseModel):
#     email: EmailStr
#     password: SecretStr

#     @validator("password")
#     def required(cls, v, values, **kwargs):
#         if not v.get_secret_value():
#             raise ValueError("password is required")
#         return v


# class User(Login):
#     full_name: str
#     confirm_password: SecretStr

#     @validator("confirm_password")
#     def passwords_match(cls, v, values, **kwargs):
#         if "password" in values and v != values["password"]:
#             raise ValueError("passwords do not match")
#         return v


class Login(BaseModel):
    email: EmailStr
    password: SecretStr

    @validator("email")
    def validate_email(cls, v, values, **kwargs):
        if not v:
            raise ValueError("Email is required")
        return v

    @validator("password")
    def required(cls, v, values, **kwargs):
        if not v.get_secret_value():
            raise ValueError("password is required")


class User(BaseModel):
    email: EmailStr
    password: SecretStr
    full_name: str
    confirm_password: SecretStr

    @validator("full_name")
    def validate_full_name(cls, v, values, **kwargs):
        if not v:
            raise ValueError("Full name is required")
        return v

    @validator("password")
    def required(cls, v, values, **kwargs):
        if not v.get_secret_value():
            raise ValueError("password is required")
        return v

    @validator("confirm_password")
    def passwords_match(cls, v, values, **kwargs):
        if v and values.get("password"):
            if v.get_secret_value() == values["password"].get_secret_value():
                return v
        raise ValueError("passwords do not match")

    @validator("email")
    def validate_email(cls, v, values, **kwargs):
        if not v:
            raise ValueError("Email is required")
        return v


class Result:
    def __init__(self, errors=None, data=None):
        self.errors = errors
        self.data = data


async def signup_user(form_data, request) -> Result:
    # import pdb
    # pdb.set_trace()
    try:
        data = User(**form_data)
    except ValidationError as e:
        errors = {x["loc"][0]: x["msg"] for x in e.errors()}
        return Result(errors=errors)
    user = await models.User.create_user(
        full_name=data.full_name, email=data.email, password=data.password
    )
    request.session["user"] = user.email
    return Result(data=data)


async def login_user(form_data, request) -> Result:
    try:
        data = Login(**form_data)
    except ValidationError as e:
        errors = {x["loc"][0]: x["msg"] for x in e.errors()}
        return Result(errors=errors)

    request.session["user"] = data.email
    return Result(data=data)


class AuthenticateError(Exception):
    pass


async def authenticate_user(user):
    if not user:
        raise AuthenticateError
    result = await models.User.objects.get(email=user)
    return user
    # if user != "james@example.com":
    #     raise AuthenticateError
    # return user

