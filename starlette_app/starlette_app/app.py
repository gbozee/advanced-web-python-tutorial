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


app = Starlette(
    routes=[
        Route("/", home, methods=["GET"]),
        Mount(
            "/static",
            StaticFiles(directory=os.path.join(BASE_DIR, "static")),
            name="static",
        ),
    ]
)


