from api.post import db


class UserData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    name = db.Column(db.String(255), nullable=False)
    national_id = db.Column(db.String(10), nullable=False, unique=True)
    ip_address = db.Column(db.String(15), nullable=False)
    photo1_s3_url = db.Column(db.String(255), nullable=False, unique=True)
    photo2_s3_url = db.Column(db.String(255), nullable=False, unique=True)
