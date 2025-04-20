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

    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_SERVER = os.getenv("DB_SERVER")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    DATABASE_URL = (f"postgresql+asyncpg://"
                    f"{DB_USER}:{DB_PASSWORD}@{DB_SERVER}:"
                    f"{DB_PORT}/{DB_NAME}")

    # S3
    MINIO_USER = os.getenv("MINIO_USER")
    MINIO_PASSWORD = os.getenv("MINIO_PASSWORD")
    MINIO_HOST = os.getenv("MINIO_HOST")
    MINIO_PORT = os.getenv("MINIO_PORT")
    BUCKET = os.getenv("BUCKET")
