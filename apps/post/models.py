from apps.post import db

from sqlalchemy.dialects import postgresql


StatusEnum = postgresql.ENUM("pending", "accepted", "rejected", name="status_enum", create_type=True)

class UserData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    name = db.Column(db.String(255), nullable=False)
    national_id = db.Column(db.String(255), nullable=False, unique=True)
    national_id_salt = db.Column(db.LargeBinary(16), nullable=False)
    ip_address = db.Column(db.String(15), nullable=False)
    photo1_s3_url = db.Column(db.String(255), nullable=False, unique=True)
    photo2_s3_url = db.Column(db.String(255), nullable=False, unique=True)
    status = db.Column(StatusEnum, default="pending", nullable=False)
