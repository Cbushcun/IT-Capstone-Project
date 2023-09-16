# IT-Capstone-Project
-----------Intro-----------
These files are all that is needed to begin testing and continue development of the Capstone Project as we proceed. 

In order to run the files properly, ensure that you have the latest release of python from here: https://www.python.org/downloads/

Once python is downloaded, ensure that you have pip installed. You can check this by going into your terminal and typing: pip --version

If this is not installed, you will need to go and install it before proceeding.

Once you are sure that pip is installed, type: pip install Flask

This will allow you to install the Flask web framework used by the application

-----------Broad explanation of the code-----------

Currently all the code will do is generate a SECRET_KEY on the initialization of the server for future use. It is printed
onto the console so that the user is able to see it and store it if needed and is then cleared from the screen as the server goes live.

There is also a few HTML pages in place to test functionality of basic links to pages and some error handling.

-----------Purpose of files-----------

All of the .html, .css, and .js files in the templates folder are currently for webpage design

routes.py - These are various functions based in Flask to handle various page routes and can be expanded upon as needed

config.py - This is the initial setup before the server goes live. Once run.py is executed, this code will run before the server is live.

\__init__.py - This is the initialization code that creates our Flask app and will import anythink into the app as needed

run.py - This is the file that you will execute in the terminal to run the app. 'use_reloader=False' ensures that the page will not be reloaded as code is changed. This setting was placed due to issues in the app restarting and then freezing potentially due to changing variables in code
