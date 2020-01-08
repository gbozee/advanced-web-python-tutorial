from flask_login import UserMixin


class AuthUser(UserMixin):
    def __init__(self, email):
        self.email = email

    def get_id(self):
        return self.email

    @classmethod
    def get(cls, user_id):
        if user_id != "james@example.com":
            return None
        return cls("james@example.com")
