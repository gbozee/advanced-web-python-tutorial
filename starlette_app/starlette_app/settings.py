from starlette.config import Config
import os
from starlette.datastructures import CommaSeparatedStrings, Secret

# Config will be read from environment variables and/or ".env" files.
config = Config(".env")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_LOCATION = os.path.join(BASE_DIR, "app.db")
DEBUG = config("DEBUG", cast=bool, default=True)
# DATABASE_URL = config('DATABASE_URL', cast=databases.DatabaseURL)
SECRET_KEY = config("SECRET_KEY", cast=Secret, default="secret key")
DATABASE_URL = config("DATABASE_URL", default=f"sqlite:///{DB_LOCATION}")

