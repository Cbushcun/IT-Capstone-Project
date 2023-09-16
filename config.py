import os # Import os module to use environment variables
import secrets # Import secrets module to generate secure SECRET_KEY
import platform  # Import the platform module to determine the OS
import subprocess # Import the subprocess module to more reliably clear the console once secret key is shared

new_secret_key = secrets.token_hex(16)
os.environ['SECRET_KEY'] = new_secret_key #Using the os module to generate SECRET_KEY through environment variables as instructed by GPT-3.5

# Print the secret key to the console
print(f'Generated Secret Key: {new_secret_key}')

# Ask the user to acknowledge the key
user_input = input("Please take note of the secret key and press Enter to clear it from the console: ")

# Clear the console (platform-independent)
# In order for this to work properly, this must be ran directly from cmd an OS equivalent. Running this from the IDE does not clear the screen (At least in personal experiences). This should not be a problem when finalized, the server should be able to be ran at a click of a button and will hopefully open an OS based terminal but would require testing to garuntee.
if platform.system() == 'Windows':
    os.system('cls' if os.name == 'nt' else 'clear')  # Try 'cls' and 'clear' for console clearing
else:
    os.system('clear') # Use 'clear' for Unix-like systems