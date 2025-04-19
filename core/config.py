import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    API_TITLE = os.getenv("API_TITLE")
    API_VERSION = os.getenv("API_VERSION")
    PROJECT_VERSION = os.getenv("PROJECT_VERSION")

    ORIGINS = [
        "*"
    ]
