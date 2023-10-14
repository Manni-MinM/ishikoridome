from apps.status.image_api.client import ImageAPIClient
from rabbitmq.client import RabbitMQClient
from s3.client import S3Client

from flask_sqlalchemy import SQLAlchemy


s3 = S3Client()
db = SQLAlchemy()
rbmq = RabbitMQClient()
imagga = ImageAPIClient()
