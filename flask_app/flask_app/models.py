from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from passlib.context import CryptContext

db = SQLAlchemy()


# class AuthUser(UserMixin):
#     def __init__(self, email):
#         self.email = email

#     def get_id(self):
#         return self.email

#     @classmethod
#     def get(cls, user_id):
#         if user_id != "james@example.com":
#             return None
#         return cls("james@example.com")


# class User()


class PasswordMixin(object):
    pwd_context = CryptContext(
        schemes=["pbkdf2_sha256", "pbkdf2_sha1", "argon2", "bcrypt_sha256"],
        deprecated="auto",
    )

    def check_password(self, password):
        return self.pwd_context.verify(password, self.password)

    def set_password(self, password):
        self.password = self.pwd_context.hash(password)


class User(db.Model, UserMixin, PasswordMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    full_name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

    def save(self):
        db.session.add(self)

    @classmethod
    def create(cls, **kwargs):
        password = kwargs.pop("password")
        instance = cls(**kwargs)
        instance.set_password(password)
        instance.save()
        return instance

    @classmethod
    def get(cls, user_id):
        return cls.query.filter_by(email=user_id).first()
