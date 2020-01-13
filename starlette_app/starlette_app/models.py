from orm import Base, utils
from pydantic import EmailStr, SecretStr
from passlib.context import CryptContext


class PasswordMixin(object):
    pwd_context = CryptContext(
        schemes=["pbkdf2_sha256", "pbkdf2_sha1", "argon2", "bcrypt_sha256"],
        deprecated="auto",
    )

    def check_password(self, password):
        value = self.password
        if isinstance(value, SecretStr):
            value = value.get_secret_value()
        return self.pwd_context.verify(password, value)

    def set_password(self, password):
        self.password = self.pwd_context.hash(password)


class User(Base, PasswordMixin):
    full_name: str
    email: EmailStr
    password: SecretStr

    class Config:
        table_name = "users"
        table_config = {
            "id": {"primary_key": True, "index": True, "unique": True},
            "email": {"index": True, "index": True, "unique": True},
        }

    @classmethod
    async def create_user(cls, **kwargs):
        result = cls(**kwargs)
        result.set_password(kwargs["password"])
        await result.save()
        return result


def init_tables(database,):
    metadata = utils.init_tables(Base, database)
    return metadata
