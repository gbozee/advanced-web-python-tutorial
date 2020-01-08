from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret

# Config will be read from environment variables and/or ".env" files.
config = Config(".env")

DEBUG = config("DEBUG", cast=bool, default=True)
# DATABASE_URL = config('DATABASE_URL', cast=databases.DatabaseURL)
SECRET_KEY = config("SECRET_KEY", cast=Secret, default="secret key")
