import os
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_app import service_layer, models, views
from flask_app.models import db
from flask_migrate import Migrate

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_LOCATION = os.path.join(BASE_DIR, "app.db")


def create_app(db_url="sqlite:///{}".format(DB_LOCATION)):
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config["SECRET_KEY"] = b"password"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    login_manager = LoginManager()
    login_manager.login_view = "login"
    login_manager.init_app(app)
    db.init_app(app)
    migrate = Migrate(app, db)

    @login_manager.user_loader
    def load_user(user_id):
        return models.User.get(user_id)

    app.register_blueprint(views.views_bp)
    return app




app = create_app()

