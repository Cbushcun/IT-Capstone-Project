import os # Import os module to use environment variables
import secrets # Import secrets module to generate secure SECRET_KEY
import platform  # Import the platform module to determine the OS
import logging

 # Logging setup
SECRET_KEY_FILE = 'secret_key.txt'
LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_FILE = 'error_log.log'

# Set up a file handler for error logs
file_handler = logging.FileHandler(LOG_FILE)
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(logging.Formatter(LOGGING_FORMAT))

# Get the root logger and add the file handler to it
logger = logging.getLogger()
logger.addHandler(file_handler)

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
    

#def get_current_user():
#    # This is just a placeholder. You need to implement this function based on your authentication system.
#    # For example, you might check if there's a user ID stored in the session and fetch the user from the database.
#    if 'user_id' in session:
#        user = fetch_user_from_database(session['user_id'])  # You need to implement fetch_user_from_database()
#        return user.name if user else None
#    return None