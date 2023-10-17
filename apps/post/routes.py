import base64
import json
import os
import uuid

from apps.post import db, s3, rbmq
from apps.post.models import UserData
from utils.hash import Hasher

from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError


routes_bp = Blueprint("routes", __name__)

def save_to_s3(file):
    _, ext = os.path.splitext(file.filename)
    filename_with_ext = f"{uuid.uuid4()}{ext}"

    return s3.put_object(file, filename_with_ext)

@routes_bp.route("/api/request/new", methods=["POST"])
def request_new():
    ip_address = request.remote_addr

    request_json = request.form["json"]
    request_json = json.loads(base64.b64decode(request_json).decode("utf-8"))

    email = request_json["email"]
    name = request_json["name"]

    national_id_salt = b""
    national_id = Hasher.hash(request_json["national_id"], salt=national_id_salt)

    photo1 = request.files['photo1']
    photo2 = request.files['photo2']

    photo1_s3_url = save_to_s3(photo1)
    photo2_s3_url = save_to_s3(photo2)

    user_data = UserData(
        ip_address=ip_address,
        email=email,
        name=name,
        national_id=national_id,
        national_id_salt=national_id_salt,
        photo1_s3_url=photo1_s3_url,
        photo2_s3_url=photo2_s3_url,
    )

    try:
        db.session.add(user_data)
        db.session.commit()

    except IntegrityError:
        db.session.rollback()
        return (jsonify({"message": "User already exists in database."}), 200)

    rbmq.publish_message(national_id)

    return (jsonify({"message": "Success"}), 200)

@routes_bp.route("/api/request/status", methods=["POST"])
def request_status():
    national_id = request.json.get("national_id")
    national_id_hashed = Hasher.hash(national_id)

    user_data = UserData.query.filter_by(national_id=national_id_hashed).first()

    if user_data is None:
        return (jsonify({"error": "No such user exists in database."}), 404)

    if request.remote_addr != user_data.ip_address:
        return (jsonify({"error": "You don't have permission to access this resource."}), 403)

    return (jsonify({"status": user_data.status}), 200)
