from apps.status import db, rbmq
from config import Config

from flask import Flask


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# FIXME: test function for now
def log(national_id):
    print(f"Received message with national_id: {national_id}")

with app.app_context():
    # TODO: error handling for connection to rbmq
    rbmq.process_messages(log)
