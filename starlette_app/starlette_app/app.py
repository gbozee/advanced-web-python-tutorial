import os
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import PlainTextResponse, RedirectResponse
from starlette.routing import Route, Mount
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from starlette.authentication import (
    requires,
    AuthenticationBackend,
    AuthCredentials,
    SimpleUser,
    AuthenticationError,
)
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette_app import service_layer, settings

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# app = Starlette()

# @app.route("/",methods=['GET'])


class AuthBackend(AuthenticationBackend):
    async def authenticate(self, request):
        # if "Authorization" not in request.headers:
        #     return
        auth = request.session.get("user")
        try:
            user_instance = service_layer.authenticate_user(auth)
        except (service_layer.AuthenticateError) as exc:
            raise AuthenticationError("Invalid auth")

        # TODO: You'd want to verify the username and password here.
        return AuthCredentials(["authenticated"]), SimpleUser(user_instance)


def home(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "form": {}, "errors": {}}
    )


def admin(request: Request):
    return templates.TemplateResponse("adminPage.html", {"request": request})


def staff(request: Request):
    return templates.TemplateResponse("staffPage.html", {"request": request})


async def login(request: Request):
    if request.method == "POST":
        form_data = await request.form()
        result = service_layer.login_user(form_data,request)
        if result.errors:
            return templates.TemplateResponse(
                "login.html",
                {"request": request, "form": form_data, "errors": result.errors},
            )
        return RedirectResponse("/user", status_code=301)
    return templates.TemplateResponse(
        "login.html", {"request": request, "form": {}, "errors": {}}
    )


async def sign_up(request: Request):
    form_data = await request.form()
    result = service_layer.signup_user(form_data)
    if result.errors:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "form": form_data, "errors": result.errors},
        )
    request.session["user"] = result.data.email
    return RedirectResponse("/user")


def logout(request: Request):
    request.session["user"] = None
    return RedirectResponse("/login")
    




def user(request: Request):
    return templates.TemplateResponse("userPage.html", {"request": request})


app = Starlette(
    debug=True,
    middleware=[
        Middleware(SessionMiddleware, secret_key=settings.SECRET_KEY,),
        Middleware(AuthenticationMiddleware, backend=AuthBackend()),
    ],
    routes=[
        Route("/", home, methods=["GET"], name="home"),
        Route("/", home, methods=["GET"], name="index"),
        Route("/admin", admin, methods=["GET"], name="admin"),
        Route("/staff", staff, methods=["GET"], name="staff"),
        Route("/login", login, methods=["GET", "POST"], name="login"),
        Route("/logout", logout, methods=["GET",], name="logout"),
        Route("/signup", sign_up, methods=["GET", "POST"], name="signup"),
        Route(
            "/user",
            requires("authenticated", redirect="login")(user),
            methods=["GET"],
            name="user",
        ),
        Mount(
            "/static",
            StaticFiles(directory=os.path.join(BASE_DIR, "static")),
            name="static",
        ),
    ],
)

