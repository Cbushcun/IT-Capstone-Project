from flask import Flask
from config import *

def create_app():
    app = Flask(__name__)
    
app = Flask(__name__)
app.secret_key = load_or_create_secret_key()
app.config.from_object('config')
app.permanant_session_lifetime = timedelta(minutes=(session_length_hours * 60))

from app import routes
