from flask import Flask
from config import *

load_secret()

def create_app():
    app = Flask(__name__)

app = Flask(__name__)
app.secret_key = get_secret()
app.config.from_object('config')
app.permanant_session_lifetime = timedelta(minutes=(session_length_hours * 60))

from app import routes
