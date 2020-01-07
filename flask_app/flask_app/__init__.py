from flask import Flask, render_template

app = Flask(__name__, template_folder="templates", static_folder="static")


@app.route("/")
def home():
    return render_template("index.html",)

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

@app.route("/userPage")
def user():
    return render_template("userPage.html",)

@app.route("/signup")
def sign_up():
    return render_template("usersignup.html",)

@app.route("/forgotpassord")
def forgot_password():
    return render_template("forgotPassword.html",)