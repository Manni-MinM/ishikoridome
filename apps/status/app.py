from apps.post import models
from apps.status import db, s3, rbmq, imagga
from apps.status.image_api import client
from config import Config

from flask import Flask


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

def face_tagged(photo_s3_url, threshold):
    photo = s3.get_object(photo_s3_url)

    try:
        res = imagga.face_detection(photo, threshold)
        return True, res["face_id"]

    except client.TaggingException as err:
        return False, None

def process(national_id):
    query = models.UserData.query.with_session(db.session)
    user_data = query.filter_by(national_id=national_id).first()

    confidence_threshold = Config.IMAGGA_TAGGER_FACE_CONFIDENCE_THRESHOLD

    try:
        photo1_has_face, photo1_face_id = face_tagged(user_data.photo1_s3_url, confidence_threshold)
        photo2_has_face, photo2_face_id = face_tagged(user_data.photo2_s3_url, confidence_threshold) 

        if photo1_has_face and photo2_has_face:
            print(f"[SUCCESS] images of user with email: {user_data.email} are valid.")

            similarity_threshold = Config.IMAGGA_SIMILARITY_CONFIDENCE_THRESHOLD
            similarity_threshold_met = imagga.face_similarity(photo1_face_id, photo2_face_id, similarity_threshold)

            if similarity_threshold_met:
                print(f"[SUCCESS] minimum similarity threshold for user with email: {user_data.email} met.")
            else:
                print(f"[FAIL] minimum similarity threshold for user with email: {user_data.email} not met.")
        else:
            print(f"[FAIL] images of user with email: {user_data.email} are invalid.")

    except Exception as err:
        print(f"[ERROR] request failed due to following error: {err}")

with app.app_context():
    # TODO: error handling for connection to rbmq
    rbmq.process_messages(process)
