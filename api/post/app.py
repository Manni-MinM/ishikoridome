import base64
import json
import os
import uuid

from config import Config
from api.post import db
from api.post.models import UserData
from s3.client import S3Client

from flask import Flask, request, jsonify
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

s3 = S3Client()

def save_to_s3(file):
    _, ext = os.path.splitext(file.filename)
    filename_with_ext = f"{uuid.uuid4()}{ext}"
    return s3.put_object(file, filename_with_ext)

@app.route("/api", methods=["POST"])
def request_api():
    ip_address = request.remote_addr

    request_json = request.form["json"]
    request_json = json.loads(base64.b64decode(request_json).decode("utf-8"))

    email = request_json["email"]
    name = request_json["name"]
    national_id = request_json["national_id"]

    photo1 = request.files['photo1']
    photo2 = request.files['photo2']

    photo1_s3_url = save_to_s3(photo1)
    photo2_s3_url = save_to_s3(photo2)

    user_data = UserData(
        ip_address=ip_address,
        email=email,
        name=name,
        national_id=national_id,
        photo1_s3_url=photo1_s3_url,
        photo2_s3_url=photo2_s3_url,
    )

    db.session.add(user_data)
    db.session.commit()

    return (jsonify({"message": "Success"}), 200)
