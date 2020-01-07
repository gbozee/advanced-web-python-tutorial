from django.http import HttpResponse
from django.shortcuts import render, redirect
from . import service_layer


def home(request):
    return render(request, "index.html", {"form": {}, "errors": {}})


def index(request):
    return render(request, "index.html", {})


def admin(request):
    return render(request, "adminPage.html", {})


def login(request):
    return render(request, "login.html", {})


def sign_up(request):
    if request.method == "POST":
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


def user(request):
    return render(request, "userPage.html", {})
