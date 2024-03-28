from app import app
from config import *
import db_setup

#Default admin login is admin@gmail.com & Password123

if __name__ == '__main__':
    try:
        db_setup.setup_database()
        try:
            register_user(admin=True)
            register_user(seller=True)
            create_auction_in_database(2, 'Initial Test Item', 'Item initialized on startup in run.py for testing purposes', '2023-11-11', '2099-12-12', '20.00')
            create_auction_in_database(2, 'Initial Expired Test Item', 'Expired item auction initialized on startup in run.py for testing purposes', '2099-10-10', '2023-10-10', '55.00')
        except sqlite3.IntegrityError as e:
            print(' * admin user already created in database')
        finally:
            log_server_start_stop('start')
            print(get_secret())
            app.run(host='0.0.0.0', port=8000, debug=True, use_reloader=False)
    finally:
        log_server_start_stop('stop')