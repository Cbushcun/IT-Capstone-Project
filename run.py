from app import app
from config import *
import db_setup
 
if __name__ == '__main__':
    try:
        db_setup.setup_database()
        log_server_start_stop('start')
        load_or_create_secret_key()
        app.run(debug=True, use_reloader=False)
    finally:
        log_server_start_stop('stop')