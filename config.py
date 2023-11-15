from collections import namedtuple
import os # Import os module to use environment variables
import secrets # Import secrets module to generate secure SECRET_KEY
import platform  # Import the platform module to determine the OS
from flask import redirect, url_for, request, render_template, session, jsonify
from db_setup import *
import logging
import sqlite3
import hashlib
import uuid
import datetime
from datetime import timedelta
import re
import stripe

admin_password = 'Password123' #Change this to alter admin and test seller password
session_length_hours = 1

stripe.api_key = 'sk_test_51O5C7EAGed7Nbg9Wt84xkDMdLyw477BQ3RcE7yq8JqKlT1CfgWcbsCjQTB8OKDQu0zw9l0mwOpjqXzxat4Orc8xV006OlHB08N'

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

#----------------------
#Server-based functions
#----------------------

def log_server_start_stop(action):
    if action == 'start':
        logger.error('-----------Server Started-----------')
    elif action == 'stop':
        logger.error('-----------Server Stopped-----------')

# Log error data to error_log.log, edit function to log user login/logout without passing as "error"
def log_data(): 
    current_user = get_current_user()
    if current_user:
        logger.error(f"User: " + get_current_user() + " IP: {request.remote_addr} - Internal Server Error - Route: {request.path}")
    else:
        ip = request.remote_addr
        route = request.path
        logger.error(f"IP: {ip} - Internal Server Error - Route: {route}")
    pass

def load_or_create_secret_key():
    clear_screen()
    try:
        with open(SECRET_KEY_FILE, 'r') as file:
            secret_key = file.read()
            #print(f"Secret key: {secret_key}")
            file.close()
            if not secret_key:
                raise FileNotFoundError
    except FileNotFoundError:
        secret_key = secrets.token_hex(16)
        with open(SECRET_KEY_FILE, 'w') as file:
            file.write(secret_key)
        #print(f"New secret key generated: {secret_key}")
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

def find_completed_auctions(bid_list):
    current_date = datetime.datetime.now().date()
    completed_auctions = []

    for auction in bid_list:
        end_time = datetime.datetime.strptime(auction['end_time'], '%Y-%m-%d').date()
        if end_time < current_date:
            completed_auctions.append(auction)

    return completed_auctions

def find_active_auctions(bid_list):
    current_date = datetime.datetime.now().date()
    active_auctions = []

    for auction in bid_list:
        end_time = datetime.datetime.strptime(auction['end_time'], '%Y-%m-%d').date()
        if end_time >= current_date:
            active_auctions.append(auction)

    return active_auctions

def has_bid_ended(item):
    current_date = datetime.datetime.now().date()
    end_time = datetime.datetime.strptime(item[5], '%Y-%m-%d').date()
    return current_date > end_time


#----------------------------------
#Functions for database informaiton
#----------------------------------
    
def hash_password(password, salt):
    """Hashes a password using SHA-256 with salt."""
    password = password.encode('utf-8')
    salt = salt.encode('utf-8')
    return hashlib.sha256(salt + password).hexdigest()

def generate_salt():
    """Generates a random salt for password hashing."""
    return uuid.uuid4().hex

def register_user(admin=False, seller=False):
    """Registers a new user in the database."""
    error = None
    if admin:
        name = 'admin'
        email = 'admin@gmail.com'
        fname = 'admin'
        lname = 'istrator'
        address = '123 admin street'
        phone_no = '000-000-0000'
        # Open a connection to your database
        conn = sqlite3.connect("auction_website.db")
        cursor = conn.cursor()
        
        # Generate a random salt and hash the password
        salt = generate_salt()
        #print('Salt generated', salt) #Debugging
        hashed_password = salt + hash_password(admin_password, salt)
        #print('hashed password', hashed_password) #Debugging

        # Insert user data into the Users table
        cursor.execute("INSERT INTO Users (username, email, password, first_name, last_name, address, phone_number) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (name, email, hashed_password, fname, lname, address, phone_no))
           
        #print('hashed_password stored') #Debugging

        conn.commit()
        conn.close()

    elif seller:
        name = 'test_seller'
        email = 'testseller@gmail.com'
        fname = 'test'
        lname = 'seller'
        address = '123 seller street'
        phone_no = '111-111-1111'
        # Open a connection to your database
        conn = sqlite3.connect("auction_website.db")
        cursor = conn.cursor()
        
        # Generate a random salt and hash the password
        salt = generate_salt()
        #print('Salt generated', salt) #Debugging
        hashed_password = salt + hash_password(admin_password, salt)
        #print('hashed password', hashed_password) #Debugging

        # Insert user data into the Users table
        cursor.execute("INSERT INTO Users (username, email, password, first_name, last_name, address, phone_number) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (name, email, hashed_password, fname, lname, address, phone_no))
           
        #print('hashed_password stored') #Debugging

        conn.commit()
        conn.close()

    else:
        if request.method == 'POST':
            email_regex = r'^[\w\.-]+@[\w\.-]+(\.\w+)+$'
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
            
            if not re.match(email_regex, email):
                error = "Invalid email address" #Does not validate if it is a live email, only verifies formatting
                return error
        
        # Check if username already exists (case-insensitive)
        cursor.execute("SELECT * FROM Users WHERE LOWER(username) = LOWER(?)", (username,))
        if cursor.fetchone():
            conn.close()
            # Handle the case where the username already exists
            error = "Username or Email already exists"
            return error

        # Check if email already exists (case-insensitive)
        cursor.execute("SELECT * FROM Users WHERE LOWER(email) = LOWER(?)", (email,))
        if cursor.fetchone():
            conn.close()
            # Handle the case where the email already exists
            error = "Username or Email already exists"
            return error
        
        # Generate a random salt and hash the password
        salt = generate_salt()
        #print('Salt generated', salt) #Debugging
        hashed_password = salt + hash_password(password, salt)
        #print('hashed password', hashed_password) #Debugging

        # Insert user data into the Users table
        cursor.execute("INSERT INTO Users (username, email, password, first_name, last_name, address, phone_number) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (username, email, hashed_password, first_name, last_name, address, phone_number))
           
        #print('hashed_password stored') #Debugging

        conn.commit()
        conn.close()
        pass  # Redirect to the index page or a dashboard after successful registration

def login_user():
    """Logs in a user and creates a session."""

    email = request.form['email']
    password = request.form['password']
    #print("DEBUG: Password and email stored for comparison") #For Debugging
    
    # Check if the email and password match a user in the Users table
    conn = sqlite3.connect("auction_website.db")
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, password FROM Users WHERE email = ?", (email,))
    user_data = cursor.fetchone()
    conn.close()
    #print("DEBUG: User Data Extracted") #For Debugging
    
    if user_data:
        user_id, hashed_password = user_data
        #print("DEBUG: User Data accessed", user_id, hashed_password) #For Debugging
        salt = hashed_password[:32]  # Extract the salt from the hashed password
        #print("DEBUG: Salt Extracted", salt) #For Debugging
        hashed_password_input = hash_password(password, salt)
        #print("DEBUG: Input password hashed with salt from stored password", hashed_password_input) #For Debugging
        
        if hashed_password == salt + hashed_password_input:
            #print("DEBUG: Hashed password == salt + hashed password") #For Debugging
            # Passwords match; create a flask session and store it in the Sessions table
            # User = namedtuple('User', [[0]'user_id',[1]'username',[2]'email',[3]'password',[4]'first_name',[5]'last_name',[6]'address',[7]'phone_number'])
            user = fetch_user_from_database(user_id)
            session['user_id'] = user[0]  
            session['session_id'] = session_id = str(uuid.uuid4())
            session['username'] = user[1]
            session['first_name'] = user[4]
            session['last_name'] = user[5]
            

            if not check_and_delete_expired_session(user[0]):
                expiration = datetime.datetime.now() + datetime.timedelta(hours=session_length_hours)  # Session expires in 1 hour
                conn = sqlite3.connect("auction_website.db")
                cursor = conn.cursor()
                cursor.execute("INSERT INTO Sessions (session_id, user_id, expiration) VALUES (?, ?, ?)",
                            (session_id, user_id, expiration))        
                conn.commit()
                conn.close()
                conn = sqlite3.connect("auction_website.db")  # Replace with your actual database path
                cursor = conn.cursor()

                # Execute an SQL query to retrieve the session_id based on the user_id
                cursor.execute("SELECT session_id FROM Sessions WHERE user_id = ?", (user_id,))
                session_data = cursor.fetchone()

                if session_data:
                    session_id = session_data[0]  # Extract the session_id from the result

                    # Close the database connection
                    conn.close()
                    
                #print("DEBUG: Passwords match, session created and stored, returning 'None', should redirect to index") #For Debugging        

            session['session_id'] = session_id

            #print("DEBUG: Flask session created ", session.get('user_id'), session.get('session_id'), session.get('username'), session.get('first_name'), session.get('last_name')) #For Debugging

            # Redirect to the main application interface
            return None
        
    error = "Invalid email or password"
    #print("DEBUG: Error, returning:", error) #For Debugging
    return error

def check_and_delete_expired_session(user_id):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect("auction_website.db")  # Replace with your actual database path
        cursor = conn.cursor()

        # Get the current date and time
        current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')[:-3]

        # Execute an SQL query to check for an existing session with the provided user_id
        cursor.execute("SELECT user_id, expiration FROM Sessions WHERE user_id = ?", (user_id,))
        session_data = cursor.fetchone()

        if session_data:
            # If a session with the user_id exists, check if it's expired
            user_id, expiration = session_data
            if expiration < current_datetime:
                # Session is expired, delete it
                cursor.execute("DELETE FROM Sessions WHERE user_id = ? AND expiration < ?", (user_id, current_datetime))
                conn.commit()
                #print("Expired session deleted") #FOR DEBUGGING
            else:
                # Session is valid
                conn.close()
                #print("Valid session found")
                return True

        # Close the database connection
        conn.close()

        return False  # No valid session found

    except sqlite3.Error as e:
        #print("SQLite error:", e)
        return False  # Failure
    
def logout_user():
    """Logs out a user, destroys the session, and removes it from the database."""
    
    #print("DEBUG: logout_user() called") #For Debugging
    conn = None  # Initialize conn to None
    #print("DEBUG: conn initialized to None") #For Debugging
    try:
        # Extract session_id from the current session
        session_id = session.get('session_id') # previous code that was here: str(session['session_id']) if 'session_id' in session else None
        user_id = session.get('user_id') # previous code that was here: str(session['user_id']) if 'user_id' in session else None
        #print("DEBUG: session_id and user_id extracted from session") #For Debugging
        
        # Validate session_id and user_id exist
        if not session_id or not user_id:
            #print("DEBUG: No session_id or user_id") #For Debugging
            raise ValueError("Invalid session data")

        # Connect to the database
        conn = sqlite3.connect("auction_website.db")
        cursor = conn.cursor()
        #print("DEBUG: Connected to database file") #For Debugging

        # Delete session data from Sessions table in the database
        cursor.execute("DELETE FROM Sessions WHERE session_id = ? AND user_id = ?", (session_id, user_id))
        conn.commit()
        #print("DEBUG: Deleted session from Sessions table expected") #For Debugging

        # Clear the user_id and any other data from the Flask session
        session.clear()
        #print("DEBUG: Session cleared from Flask session") #For Debugging

        # Optionally, log the user's logout activity
        #log_data()  # Assuming log_data function logs user activities including logout
        # #print("DEBUG: Data Logged") #For Debugging

        # Redirect to the login page or the home page after logout
        #print("DEBUG: Redirecting to login") #For Debugging
        return redirect(url_for('login'))  # Replace 'login' with the endpoint for your login page

    except ValueError as ve:
        # Handle invalid session data error
        #print(f"Error: {ve}")
        return redirect(url_for('login'))  # Redirect to login on error

    except sqlite3.Error as e:
        # Handle database error
        #print(f"Database error: {e}")
        return redirect(url_for('login'))  # Redirect to login on error

    finally:
        # Ensure the database connection is closed
        if conn:  # Check if conn is not None before trying to close it
            conn.close()
            
def get_username_by_user_id(user_id):
    try:
        # Establish a connection to the SQLite database
        conn = sqlite3.connect("auction_website.db")
        cursor = conn.cursor()

        # Execute a SQL query to fetch the username based on user_id
        cursor.execute("SELECT username FROM Users WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()

        if result:
            # If a matching user is found, return their username
            return result[0]

        # If no user with the given user_id is found, return None
        return None

    except sqlite3.Error as e:
        # Handle any potential database errors here
        ##print(f"Database error: {e}")
        return None

    finally:
        # Close the database connection when done
        conn.close()

    # Example usage:
    #user_id = 1  # Replace with the actual user_id of the current user
    #username = get_username_by_user_id(user_id)

def get_current_user():
    if 'user_id' in session:
        user = fetch_user_from_database(session['user_id'])  
        return user.username if user else None
    return None
  
def fetch_user_from_database(user_id):
    """
    Fetch a user from the database using the user_id.

    :param user_id: The ID of the user to fetch
    :return: A user object or None if no user is found
    """
    conn = sqlite3.connect('auction_website.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users WHERE user_id = ?", (user_id,))
    user_data = cursor.fetchone()
    conn.close()

    if user_data:
        # You might want to map the user_data to a User object or dictionary here
        # This is just a simple example, you need to replace this with your actual User class or data structure
        User = namedtuple('User', ['user_id', 'username', 'email', 'password', 'first_name', 'last_name', 'address', 'phone_number'])
        user = User(*user_data)
        return user
    else:
        return None
 
def create_auction_in_database( item_seller_id, item_name, item_desc, item_start_time, item_end_time, item_reserve_price):

    """Creates a new auction listing in the database."""
    seller_id = item_seller_id
    title = item_name
    description = item_desc
    start_time = item_start_time
    end_time = item_end_time
    reserve_price = item_reserve_price

    # Insert auction data into the Auctions table
    conn = sqlite3.connect("auction_website.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Auctions (seller_id, title, description, start_time, end_time, reserve_price) VALUES (?, ?, ?, ?, ?, ?)",
                   (seller_id, title, description, start_time, end_time, reserve_price))  # Replace '1' with the actual seller's user_id
    conn.commit()
    conn.close()

def get_most_recent_auction_id():
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect("auction_website.db")
        cursor = conn.cursor()

        # Execute a SQL query to retrieve the most recent auction_id
        cursor.execute("SELECT auction_id FROM Auctions ORDER BY auction_id DESC LIMIT 1")
        most_recent_auction_id = cursor.fetchone()

        # Close the database connection
        conn.close()

        if most_recent_auction_id:
            return most_recent_auction_id[0]  # Extract the auction_id from the tuple
        else:
            return None  # No entries in the table

    except sqlite3.Error as e:
        #print("SQLite error:", e)
        return None
    
def get_most_recent_auction():
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect("auction_website.db")
        cursor = conn.cursor()

        # Execute a SQL query to retrieve the most recent entry in the "Auctions" table
        cursor.execute("SELECT * FROM Auctions ORDER BY auction_id DESC LIMIT 1")
        most_recent_auction = cursor.fetchone()

        # Close the database connection
        conn.close()

        return most_recent_auction


    except sqlite3.Error as e:
        #print("SQLite error:", e)
        return None
    
def find_auction_by_id(auction_id):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect("auction_website.db")
        cursor = conn.cursor()

        # Execute a SQL query to retrieve the row with the specified auction_id
        cursor.execute("SELECT * FROM Auctions WHERE auction_id = ?", (auction_id,))
        result = cursor.fetchone()

        # Close the database connection
        conn.close()

        return result  # Returns the row as a tuple

    except sqlite3.Error as e:
        #print("SQLite error:", e)
        return None
    
def update_reserve_price(auction_id, new_reserve_price):
    print('update reserve price called')
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect("auction_website.db")
        cursor = conn.cursor()
        print('connected to db')

        # Execute an SQL query to update the reserve_price for the specified auction_id
        cursor.execute("UPDATE Auctions SET reserve_price = ? WHERE auction_id = ?", (new_reserve_price, auction_id))
        print('updated')
        # Commit the changes and close the database connection

        conn.commit()
        print('conn commited')
        conn.close()
        print('conn closed')
        return True  # Success

    except sqlite3.Error as e:
        print("SQLite error:", e)
        return False  # Failure

def get_unexpired_auctions():
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect("auction_website.db")
        cursor = conn.cursor()

        # Get the current date and time
        current_datetime = datetime.datetime.now()

        # Execute a SQL query to retrieve unexpired auctions
        cursor.execute("SELECT auction_id, seller_id, title, description, end_time, reserve_price FROM Auctions WHERE end_time > ?", (current_datetime,))
        unexpired_auctions = cursor.fetchall()
        # Close the database connection
        conn.close()

        # Convert the fetched data to a list of dictionaries
        auction_data = []
        for row in unexpired_auctions:
            auction_id, seller_id, title, description, end_time, reserve_price = row
            seller_name = get_username_by_user_id(seller_id)
            auction_data.append({
                'auction_id': auction_id,
                'seller_name': seller_name,
                'title': title,
                'description': description,
                'end_time': end_time,
                'reserve_price': reserve_price
            })

        return auction_data
    
    except sqlite3.Error as e:
        #print("SQLite error:", e)
        return False  # Failure

def get_expired_auctions():
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect("auction_website.db")
        cursor = conn.cursor()

        # Get the current date and time
        current_datetime = datetime.datetime.now()

        # Execute a SQL query to retrieve unexpired auctions
        cursor.execute("SELECT auction_id, seller_id, title, description, end_time, reserve_price FROM Auctions WHERE end_time < ?", (current_datetime,))
        unexpired_auctions = cursor.fetchall()
        # Close the database connection
        conn.close()

        # Convert the fetched data to a list of dictionaries
        auction_data = []
        for row in unexpired_auctions:
            auction_id, seller_id, title, description, end_time, reserve_price = row
            seller_name = get_username_by_user_id(seller_id)
            auction_data.append({
                'auction_id': auction_id,
                'seller_name': seller_name,
                'title': title,
                'description': description,
                'end_time': end_time,
                'reserve_price': reserve_price
            })

        return auction_data
    
    except sqlite3.Error as e:
        #print("SQLite error:", e)
        return None
