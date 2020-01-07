import os
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.routing import Route, Mount
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
import uvicorn

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# app = Starlette()

# @app.route("/",methods=['GET'])


def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

def admin(request: Request):
    return templates.TemplateResponse("adminPage.html", {"request": request})

def staff(request: Request):
    return templates.TemplateResponse("staffPage.html", {"request": request})

def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

def sign_up(request: Request):
    return templates.TemplateResponse("usersignup.html", {"request": request})

def user(request: Request):
    return templates.TemplateResponse("userPage.html", {"request": request})


app = Starlette(
    routes=[
        Route("/", home, methods=["GET"]),
        Route("/", index, methods=["GET"]),
        Route("/admin", admin, methods=["GET"]),
        Route("/staff", staff, methods=["GET"]),
        Route("/login", login, methods=["GET"]),
        Route("/signup", sign_up, methods=["GET"]),
        Route("/user", user, methods=["GET"]),
        Mount(
            "/static",
            StaticFiles(directory=os.path.join(BASE_DIR, "static")),
            name="static",
        ),
    ]
)

