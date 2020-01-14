from flask import Blueprint, render_template, request, redirect, url_for
from flask_app import service_layer
from flask_login import login_required, logout_user

views_bp = Blueprint("views", __name__, url_prefix="/")


@views_bp.route("/")
def home():
    return render_template("index.html", **{"form": {}, "errors": {}})


@views_bp.route("/admin")
def admin():
    return render_template("adminPage.html",)


@views_bp.route("/about")
def about():
    return render_template("index.html",)


@views_bp.route("/services")
def services():
    return render_template("index.html",)


@views_bp.route("/staff")
def staff():
    return render_template("staffPage.html",)


@views_bp.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        result = service_layer.login_user(request.form)
        if result.errors:
            return render_template(
                "login.html", **{"form": request.form, "errors": result.errors}
            )
        return redirect("user")
    return render_template("login.html", **{"form": {}, "errors": {}})


@views_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))


@views_bp.route("/user")
@login_required
def user():
    return render_template("userPage.html",)


@views_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        result = service_layer.signup_user(request.form)
        if result.errors:
            return render_template(
                "index.html", **{"form": request.form, "errors": result.errors}
            )
        return redirect("user",)
    return render_template("index.html", **{"form": {}, "errors": {}})


# @views_bp.route("/signup", methods=["GET", "POST"])
# def signup():
#     result = service_layer.signup_user(request.form)
#     if result.errors:
#         return render_template(
#             "index.html", **{"form": request.form, "errors": result.errors}
#         )
#     return redirect("user")


@views_bp.route("/forgotpassword")
def forgot_password():
    return render_template("forgotPassword.html",)
