from flask import Flask, render_template, request, redirect
from flask_app import service_layer

app = Flask(__name__, template_folder="templates", static_folder="static")


@app.route("/")
def home():
    return render_template("index.html", **{"form": {}, "errors": {}})


@app.route("/")
def index():
    return render_template("index.html",)


@app.route("/admin")
def admin():
    return render_template("adminPage.html",)


@app.route("/about")
def about():
    return render_template("index.html",)


@app.route("/services")
def services():
    return render_template("index.html",)


@app.route("/staff")
def staff():
    return render_template("staffPage.html",)


@app.route("/login")
def login():
    return render_template("login.html",)


@app.route("/user")
def user():
    return render_template("userPage.html",)


@app.route("/signup", methods=["POST"])
def signup():
    data = request.form
    result = service_layer.signup_user(request.form)
    if result.errors:
        return render_template(
            "index.html", **{"form": data, "errors": result.errors}
        )
    return redirect("user")


@app.route("/forgotpassord")
def forgot_password():
    return render_template("forgotPassword.html",)
