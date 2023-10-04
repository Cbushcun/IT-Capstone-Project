from app import app
from config import *

if __name__ == '__main__':
    load_or_create_secret_key()
    app.run(debug=True, use_reloader=False)