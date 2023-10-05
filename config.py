import os # Import os module to use environment variables
import secrets # Import secrets module to generate secure SECRET_KEY
import platform  # Import the platform module to determine the OS
from flask import redirect, url_for, request, render_template
from db_setup import *
import logging
import sqlite3
import hashlib
import uuid
import datetime

# Logging setup
SECRET_KEY_FILE = 'secret_key.txt'
LOGGING_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
LOG_FILE = 'error_log.log'

# Set up a file handler for error logs
file_handler = logging.FileHandler(LOG_FILE)
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(logging.Formatter(LOGGING_FORMAT))

# Get the root logger and add the file handler to it
logger = logging.getLogger()
logger.addHandler(file_handler)

#Server configs
def log_server_start_stop(action):
    if action == 'start':
        logger.error('-----------Server Started-----------')
    elif action == 'stop':
        logger.error('-----------Server Stopped-----------')
     
def load_or_create_secret_key():
    clear_screen();
    try:
        with open(SECRET_KEY_FILE, 'r') as file:
            secret_key = file.read()
            print(f"Secret key: {secret_key}")
            file.close();
            clear_screen_and_get_input()
            if not secret_key:
                raise FileNotFoundError
    except FileNotFoundError:
        secret_key = secrets.token_hex(16)
        with open(SECRET_KEY_FILE, 'w') as file:
            file.write(secret_key)
        print(f"New secret key generated: {secret_key}")
        clear_screen_and_get_input()
    return secret_key

def clear_screen_and_get_input():
    user_input = input("Do you want to generate a new secret key? (Y/N): ")
    clear_screen()
    if user_input.lower() == 'y':
        generate_new_secret_key()
    

def generate_new_secret_key():
    os.remove(SECRET_KEY_FILE)
    load_or_create_secret_key()
    
def clear_screen():
    # Clear the console (platform-independent
    if platform.system() == 'Windows':
        os.system('cls' if os.name == 'nt' else 'clear')  # Try 'cls' and 'clear' for console clearing
    else:
        os.system('clear') # Use 'clear' for Unix-like systems
        
#Database Config
    
def hash_password(password, salt):
    """Hashes a password using SHA-256 with salt."""
    password = password.encode('utf-8')
    salt = salt.encode('utf-8')
    return hashlib.sha256(salt + password).hexdigest()

def generate_salt():
    """Generates a random salt for password hashing."""
    return uuid.uuid4().hex

def register_user():
    """Registers a new user in the database."""
    error = None
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        first_name = request.form.get('first_name')  # .get() allows for the value to be None if it's not provided
        last_name = request.form.get('last_name')
        address = request.form.get('address')
        phone_number = request.form.get('phone_number')

        # Open a connection to your database
        conn = sqlite3.connect("auction_website.db")
        cursor = conn.cursor()
        
        # Check if username already exists (case-insensitive)
        cursor.execute("SELECT * FROM Users WHERE LOWER(username) = LOWER(?)", (username,))
        if cursor.fetchone():
            conn.close()
            # Handle the case where the username already exists
            error = "Username or Email already exists"
            return error  # HTTP status code 400 represents a bad request

        # Check if email already exists (case-insensitive)
        cursor.execute("SELECT * FROM Users WHERE LOWER(email) = LOWER(?)", (email,))
        if cursor.fetchone():
            conn.close()
            # Handle the case where the email already exists
            error = "Username or Email already exists"
            return error  # HTTP status code 400 represents a bad request
        
        # Generate a random salt and hash the password
        salt = generate_salt()
        hashed_password = hash_password(password, salt)

        # Insert user data into the Users table
        cursor.execute("INSERT INTO Users (username, email, password, first_name, last_name, address, phone_number) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (username, email, hashed_password, first_name, last_name, address, phone_number))
        # Get user input

        conn.commit()
        conn.close()
        pass  # Redirect to the index page or a dashboard after successful registration

def login_user():
    """Logs in a user and creates a session."""
    username = login_username_entry.get()
    password = login_password_entry.get()

    # Check if the username and password match a user in the Users table
    conn = sqlite3.connect("auction_website.db")
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, password FROM Users WHERE username = ?", (username,))
    user_data = cursor.fetchone()
    conn.close()

    if user_data:
        user_id, hashed_password = user_data
        salt = hashed_password[:64]  # Extract the salt from the hashed password
        if hashed_password == hash_password(password, salt):
            # Passwords match; create a session and store it in the Sessions table
            session_id = str(uuid.uuid4())
            expiration = datetime.datetime.now() + datetime.timedelta(hours=1)  # Session expires in 1 hour
            conn = sqlite3.connect("auction_website.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Sessions (session_id, user_id, expiration) VALUES (?, ?, ?)",
                           (session_id, user_id, expiration))
            conn.commit()
            conn.close()

            # Redirect to the main application interface (you can implement this)
            show_auction_interface()

def create_auction():
    """Creates a new auction listing in the database."""
    title = auction_title_entry.get()
    description = auction_description_entry.get()
    start_time = auction_start_time_entry.get()
    end_time = auction_end_time_entry.get()
    reserve_price = auction_reserve_price_entry.get()

    # Insert auction data into the Auctions table
    conn = sqlite3.connect("auction_website.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Auctions (seller_id, title, description, start_time, end_time, reserve_price) VALUES (?, ?, ?, ?, ?, ?)",
                   (1, title, description, start_time, end_time, reserve_price))  # Replace '1' with the actual seller's user_id
    conn.commit()
    conn.close()


#def get_current_user():
#    # This is just a placeholder. You need to implement this function based on your authentication system.
#    # For example, you might check if there's a user ID stored in the session and fetch the user from the database.
#    if 'user_id' in session:
#        user = fetch_user_from_database(session['user_id'])  # You need to implement fetch_user_from_database()
#        return user.name if user else None
#    return None