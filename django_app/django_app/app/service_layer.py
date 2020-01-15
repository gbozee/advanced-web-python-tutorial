from logging import error
from pydantic import BaseModel, EmailStr, SecretStr, validator, ValidationError
from django import forms
from django.contrib.auth.models import User as BaseUser
from django.contrib.auth import authenticate, login as _login_user
from django.db import IntegrityError


class AuthenticateError(Exception):
    pass

def database_auth(user):
    if user.username ==  user:
        raise AuthenticateError
    return user

def authenticate_user(user):
    if not user:
        raise AuthenticateError
    return user


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()

    def login_user(self, request):
        user = authenticate(
            request,
            username=self.cleaned_data["email"],
            password=self.cleaned_data["password"],
        )
        # user = User.objects.get(email=self.cleaned_data['email'])
        # f user.check_password(self.cleaned_data['password'])
        try:
            user = authenticate_user(user)
        except AuthenticateError:
            return None
        if user.check_password(self.cleaned_data["password"]):
            _login_user(request, user)
            return user

        # if user is not None:
        # return user


class UserForm(LoginForm):
    full_name = forms.CharField()
    confirm_password = forms.CharField()
        
    

    def clean(self):
        data = super().clean()
        password = data.get("password")
        username= data.get("email")
        if username == "james@example.com":
            self.add_error("email", "Email already exist")
        confirm_password = data.get("confirm_password")
        if password and confirm_password:
            if password != confirm_password:
                self.add_error("confirm_password", "Password is not the same")
                
            
        return data

    def save(self):
        user = BaseUser.objects.create(
            username=self.cleaned_data["email"],
            email=self.cleaned_data["email"],
            first_name=self.cleaned_data["full_name"],
        )
        user.set_password(self.cleaned_data["password"])
        user.save()
        # password=self.cleaned_data["password"],
        return user


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
    
    # @validator("username")
    # def validate_useername()
    # try:
    # # code that produces error
    # except IntegrityError as e:
    # return render_to_response("template.html", {"message": e.message})


class Role(User):
    role = str


class Result:
    def __init__(self, errors=None, data=None):
        self.errors = errors
        self.data = data


def signup_user(form_data) -> Result:

    form = UserForm(data=form_data)
    
    if not form.is_valid():
        return Result(errors=form.errors)
    result = form.save()
    return Result(data=result)


def login_user(form_data, request) -> Result:
    form = LoginForm(data=form_data)
    if not form.is_valid():
        return Result(errors=form.errors)
    user = form.login_user(request)
    if not user:
        return Result(errors={"email": "Could not login user"})
    return Result(data=user)

