import os

from dotenv import load_dotenv


load_dotenv()

class Config:
    DB_HOST = os.environ.get("DB_HOST", "")
    DB_NAME = os.environ.get("DB_NAME", "")
    DB_PORT = os.environ.get("DB_PORT", "5432")
    DB_USER = os.environ.get("DB_USER", "root")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "root")
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    S3_ACCESS_KEY = os.environ.get("S3_ACCESS_KEY", "")
    S3_SECRET_KEY = os.environ.get("S3_SECRET_KEY", "")
    S3_ENDPOINT_URL = os.environ.get("S3_ENDPOINT_URL", "")
    S3_BUCKET_NAME= os.environ.get("S3_BUCKET_NAME", "")
    S3_CONNECTION_RETRIES = int(os.environ.get("S3_CONNECTION_RETRIES", "3"))
    S3_CONNECTION_TIMEOUT_SECONDS = int(os.environ.get("S3_CONNECTION_TIMEOUT_SECONDS", "60"))
    RBMQ_HOST = os.environ.get("RBMQ_HOST", "")
    RBMQ_PORT = os.environ.get("RBMQ_PORT", "")
    RBMQ_USER = os.environ.get("RBMQ_USER", "")
    RBMQ_PASSWORD = os.environ.get("RBMQ_PASSWORD", "")
    RBMQ_VIRTUAL_HOST = os.environ.get("RBMQ_VIRTUAL_HOST", "/")
    RBMQ_CONNECTION_RETRIES = int(os.environ.get("RBMQ_CONNECTION_RETRIES", "3"))
    RBMQ_RETRY_DELAY_SECONDS = int(os.environ.get("RBMQ_RETRY_DELAY_SECONDS", "5"))
    RBMQ_CONNECTION_TIMEOUT_SECONDS = int(os.environ.get("RBMQ_CONNECTION_TIMEOUT_SECONDS", "15"))
    RBMQ_QUEUE_NAME = os.environ.get("RBMQ_QUEUE_NAME", "")
    IMAGGA_API_KEY = os.environ.get("IMAGGA_API_KEY", "")
    IMAGGA_API_SECRET = os.environ.get("IMAGGA_API_SECRET", "")
    IMAGGA_CLIENT_RETRIES = int(os.environ.get("IMAGGA_CLIENT_RETRIES", "3"))
    IMAGGA_CLIENT_TIMEOUT_SECONDS = int(os.environ.get("IMAGGA_CLIENT_TIMEOUT_SECONDS", "60"))
    IMAGGA_TAGGER_FACE_CONFIDENCE_THRESHOLD = float(os.environ.get("IMAGGA_TAGGER_FACE_CONFIDENCE_THRESHOLD", "75.0"))
    IMAGGA_SIMILARITY_CONFIDENCE_THRESHOLD = float(os.environ.get("IMAGGA_SIMILARITY_CONFIDENCE_THRESHOLD", "80.0"))
