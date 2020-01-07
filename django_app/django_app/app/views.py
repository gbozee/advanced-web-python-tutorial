from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return render(request, "index.html", {})

def index(request):
    return render(request, "index.html", {})

def admin(request):
    return render(request, "adminPage.html", {})


def login(request):
    return render(request, "login.html", {})

def sign_up(request):
    return render(request, "usersignup.html", {})

def staff(request):
    return render(request, "staffPage.html", {})

def user(request):
    return render(request, "userPage.html", {})
