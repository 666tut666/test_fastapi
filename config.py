import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")
##.env file load garya postgres ko setting ko lai


class Settings:
    TITLE="title from config"
    VERSION = "0.0.1"
    DESCRIPTION = "dummy project description"
    NAME = "USER"
    EMAIL = "mail@email.com"

    POSTGRES_USER = os.getenv("POSTGRES_USER")
    ##os.getenv pulls pull env variable from .env
    ##it loads from .env file rather than system
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", 5432)
    POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE", "testing")
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{POSTGRES_DATABASE}"
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = "HS256"
    TEST_EMAIL = "user1@test.com"
    TEST_PASS = "password"
    TEST_ITEM = "test item"
    TEST_ITEM_DEF = "item description"


setting = Settings()
