from api.post import db


class UserData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    national_id = db.Column(db.String(10), unique=True, nullable=False)
    ip_address = db.Column(db.String(15), nullable=False)
    photo1 = db.Column(db.LargeBinary, nullable=False)
    photo2 = db.Column(db.LargeBinary, nullable=False)
