import os # Import os module to use environment variables
import secrets # Import secrets module to generate secure SECRET_KEY
import platform  # Import the platform module to determine the OS

SECRET_KEY_FILE = 'secret_key.txt'

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