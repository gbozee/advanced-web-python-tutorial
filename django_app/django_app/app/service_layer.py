from logging import error
from pydantic import BaseModel, EmailStr, SecretStr, validator, ValidationError
from django import forms


class UserForm(forms.Form):
    full_name = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField()
    confirm_password = forms.CharField()

    def clean(self):
        data = super().clean()
        password = data.get("password")
        confirm_password = data.get("confirm_password")
        if password and confirm_password:
            if password != confirm_password:
                self.add_error("confirm_password", "Password is not the same")
        return data

    
class User(BaseModel):
    full_name: str
    email: EmailStr
    password: SecretStr
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
    # try:
    #     data = User(**form_data)
    # except ValidationError as e:
    #     errors = {x["loc"][0]: x["msg"] for x in e.errors()}
    # return Result(errors=errors)
    form = UserForm(data=form_data)
    if not form.is_valid():
        return Result(errors=form.errors)
    return Result(data=form.cleaned_data)


def login_user(form_data) -> Result:
    form = UserForm(data=form_data)
    if not form.is_valid():
        return Result(errors=form.errors)
    return Result(data=form.cleaned_data)
    