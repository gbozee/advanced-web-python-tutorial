from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, login_required
from flask_app import service_layer, models

app = Flask(__name__, template_folder="templates", static_folder="static")
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


app.secret_key = b"password"


@login_manager.user_loader
def load_user(user_id):
    return models.AuthUser.get(user_id)


@app.route("/")
def home():
    return render_template("index.html", **{"form": {}, "errors": {}})


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


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        result = service_layer.login_user(request.form)
        if result.errors:
            return render_template(
                "login.html", **{"form": request.form, "errors": result.errors}
            )
        login_user(models.AuthUser(result.data.email))
        return redirect("user",)
    return render_template("login.html", **{"form": {}, "errors": {}})


@app.route("/logout")
def logout():
    # session.clear()
    return redirect(url_for("home"))


@app.route("/user")
@login_required
def user():
    return render_template("userPage.html",)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        result = service_layer.signup_user(request.form)
        if result.errors:
            return render_template("index.html", **{"form": request.form, "errors": result.errors})
        login_user(models.AuthUser(result.data.email))
        return redirect("user",)
    return render_template("index.html", **{"form": {}, "errors": {}})

# @app.route("/signup", methods=["GET", "POST"])
# def signup():
#     result = service_layer.signup_user(request.form)
#     if result.errors:
#         return render_template(
#             "index.html", **{"form": request.form, "errors": result.errors}
#         )
#     return redirect("user")




@app.route("/forgotpassword")
def forgot_password():
    return render_template("forgotPassword.html",)
