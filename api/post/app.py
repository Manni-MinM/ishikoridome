import json
import base64

from config import Config
from api.post import db
from api.post.models import UserData

from flask import Flask, request, jsonify
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

@app.route("/api", methods=["POST"])
def request_api():
    ip_address = request.remote_addr

    request_json = request.form["json"]
    request_json = json.loads(base64.b64decode(request_json).decode("utf-8"))

    email = request_json["email"]
    name = request_json["name"]
    national_id = request_json["national_id"]

    photo1 = request.files['photo1'].read()
    photo2 = request.files['photo2'].read()

    user_data = UserData(
        ip_address=ip_address,
        email=email,
        name=name,
        national_id=national_id,
        photo1=photo1,
        photo2=photo2,
    )

    db.session.add(user_data)
    db.session.commit()

    return (jsonify({"message": "Success"}), 200)
