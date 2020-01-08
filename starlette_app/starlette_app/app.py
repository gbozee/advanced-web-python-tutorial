import os
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import PlainTextResponse, RedirectResponse
from starlette.routing import Route, Mount
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
import uvicorn
from starlette_app import service_layer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# app = Starlette()

# @app.route("/",methods=['GET'])


def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "form": {},"errors":{}})


def admin(request: Request):
    return templates.TemplateResponse("adminPage.html", {"request": request})


def staff(request: Request):
    return templates.TemplateResponse("staffPage.html", {"request": request})


async def login(request: Request):
    if request.method == "GET":
        return templates.TemplateResponse("login.html", {"request": request,"form":{},"errors":{}})
    else:
        form_data = await request.form()
        result = service_layer.login_user(form_data)
        if result.errors:
            return templates.TemplateResponse(
            "login.html",
            {"request":request,"form":form_data, "errors":result.errors},
        )
        return RedirectResponse("/user")


async def sign_up(request: Request):
    form_data = await request.form()
    result = service_layer.signup_user(form_data)
    if result.errors:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "form": form_data, "errors": result.errors},
        )
    return RedirectResponse("/user")


def user(request: Request):
    return templates.TemplateResponse("userPage.html", {"request": request})


app = Starlette(
    debug=True,
    routes=[
        Route("/", home, methods=["GET"], name="home"),
        Route("/", home, methods=["GET"], name="index"),
        Route("/admin", admin, methods=["GET"], name="admin"),
        Route("/staff", staff, methods=["GET"], name="staff"),
        Route("/login", login, methods=["GET","POST"], name="login"),
        Route("/signup", sign_up, methods=["GET","POST"], name="signup"),
        Route("/user", user, methods=["GET"], name="user"),
        Mount(
            "/static",
            StaticFiles(directory=os.path.join(BASE_DIR, "static")),
            name="static",
        ),
    ],
)

