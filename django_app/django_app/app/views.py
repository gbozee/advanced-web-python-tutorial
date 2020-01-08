from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import service_layer


def home(request):
    return render(request, "index.html", {"form": {}, "errors": {}})


def index(request):
    return render(request, "index.html", {})


def admin(request):
    return render(request, "adminPage.html", {})


def login(request):
    if request.method == "GET":
        return render(request, "login.html", {})
    else:
        result = service_layer.login_user(request.POST.dict(), request)
        if result.errors:
            return render(
                request,
                "login.html",
                {"form": request.POST.dict(), "errors": result.errors},
            )
    return redirect("user")


def sign_up(request):
    if request.method == "GET":
        return render(request, "index.html", {})
    else:
        result = service_layer.signup_user(request.POST.dict())
        if result.errors:
            return render(
                request,
                "index.html",
                {"form": request.POST.dict(), "errors": result.errors},
            )
    return redirect("user")


def staff(request):
    return render(request, "staffPage.html", {})


@login_required(login_url="/login")
def user(request):
    return render(request, "userPage.html", {})
