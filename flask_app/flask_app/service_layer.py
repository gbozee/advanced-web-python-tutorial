from pydantic import BaseModel, EmailStr, SecretStr, validator, ValidationError


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


class User(Login):
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
    return Result(data=data)


def login_user(form_data) -> Result:
    try:
        data = Login(**form_data)
    except ValidationError as e:
        errors = {x["loc"][0]: x["msg"] for x in e.errors()}
        return Result(errors=errors)
    return Result(data=data)
