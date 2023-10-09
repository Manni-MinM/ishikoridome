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

    # TODO: refactor storing photos on s3
    _, photo1_ext = os.path.splitext(photo1.filename)
    _, photo2_ext = os.path.splitext(photo2.filename)

    photo1_s3_url = s3.put_object(photo1, f"{uuid.uuid4()}{photo1_ext}")
    photo2_s3_url = s3.put_object(photo2, f"{uuid.uuid4()}{photo2_ext}")

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
