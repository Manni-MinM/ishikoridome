import logging

from apps.post import models
from apps.status import db, s3, rbmq, imagga, mailgun
from apps.status.image_api import client
from config import Config

from flask import Flask


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

log_handler = logging.StreamHandler()
log_handler.setLevel(logging.INFO)
log_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s: %(message)s")
)

logger.addHandler(log_handler)

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
            logger.info(f"[SUCCESS] images of user with email: {user_data.email} are valid.")

            similarity_threshold = Config.IMAGGA_SIMILARITY_CONFIDENCE_THRESHOLD
            similarity_threshold_met = imagga.face_similarity(photo1_face_id, photo2_face_id, similarity_threshold)

            if similarity_threshold_met:
                user_data.status = "accepted"
                logger.info(f"[SUCCESS] minimum similarity threshold for user with email: {user_data.email} met.")
            else:
                user_data.status = "rejected"
                logger.error(f"[FAIL] minimum similarity threshold for user with email: {user_data.email} not met.")
        else:
            user_data.status = "rejected"
            logger.error(f"[FAIL] images of user with email: {user_data.email} are invalid.")

    except Exception as err:
        logger.critical(f"[CRITICAL] request failed due to following error: {err}")

    db.session.commit()

    try:
        subject = "Your request has been processed"
        text = f"Your request status has changed to {user_data.status}."
        mailgun.send_mail(user_data.email, subject, text)
        logger.info(f"[SUCCESS] sent status update mail for user with email: {user_data.email}.")

    except Exception as err:
        logger.critical(f"[CRITICAL] failed to send email due to following error: {err}")

with app.app_context():
    rbmq.process_messages(process)
