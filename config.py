import os

from dotenv import load_dotenv


load_dotenv()

class Config:
    DEBUG = True
    DB_HOST = os.environ.get("DB_HOST", "")
    DB_NAME = os.environ.get("DB_NAME", "")
    DB_PORT = os.environ.get("DB_PORT", "5432")
    DB_USER = os.environ.get("DB_USER", "root")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "root")
    # TODO: add s3 keys
    S3_ACCESS_KEY = "<dummy>"
    S3_SECRET_KEY = "<dummy>"
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
