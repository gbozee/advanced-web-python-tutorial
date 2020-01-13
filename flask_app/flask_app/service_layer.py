from pydantic import BaseModel, EmailStr, SecretStr, validator, ValidationError
from flask_login import login_user as _login_user
from . import models


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

    @validator("confirm_password")
    def passwords_match(cls, v, values, **kwargs):
        if "password" in values and v != values["password"]:
            raise ValueError("passwords do not match")
        return v

    @validator("email")
    def validate_email(cls, v, values, **kwargs):
        if not v:
            raise ValueError("Email is required")
        return v

    @validator("password")
    def required(cls, v, values, **kwargs):
        if not v.get_secret_value():
            raise ValueError("password is required")
        return v


class Result:
    def __init__(self, errors=None, data=None):
        self.errors = errors
        self.data = data


def signup_user(form_data) -> Result:
    # import pdb

    # pdb.set_trace()
    try:
        data = User(**form_data)
    except ValidationError as e:
        errors = {x["loc"][0]: x["msg"] for x in e.errors()}
        return Result(errors=errors)
    user = models.User.create(
        full_name=data.full_name,
        email=data.email,
        password=data.password.get_secret_value(),
    )
    _login_user(user)
    return Result(data=data)


def login_user(form_data) -> Result:
    try:
        data = Login(**form_data)
    except ValidationError as e:
        errors = {x["loc"][0]: x["msg"] for x in e.errors()}
        return Result(errors=errors)
    login_user(models.User.get(data.email))
    return Result(data=data)
