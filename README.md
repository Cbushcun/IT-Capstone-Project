# IT-Capstone-Project
-----------Intro-----------
These files are all that is needed to begin testing and continue development of the Capstone Project as we proceed. 

In order to run the files properly, ensure that you have the latest release of python from here: https://www.python.org/downloads/

Once python is downloaded, ensure that you have pip installed. You can check this by going into your terminal and typing: pip --version

If this is not installed, you will need to go and install it before proceeding.

Once you are sure that pip is installed, type: pip install Flask

This will allow you to install the Flask web framework used by the application

__IMPORTANT: When you are working on this project, ensure that you are actively working on a new branch or working with local files to protect any current working copy of the site. This will require knowledge on how to use GitHub pull, push, and merge features depending on the method you choose to use GitHub functions (terminal, GitHub desktop, GitHub in Visual Studio, and any other way you may access it)__

-----------Broad explanation of the code-----------

Currently all the code will do is generate a SECRET_KEY and display it on the console for any future use it may have as well as begin a local server for you to view the website. The security key is printed onto the console so that the user is able to see it and store it if needed and is then cleared from the screen as the server goes live. You can access the webapp once the server is launched by going to the IP that is listed on the console once the server is running on your machine.

There is also a few HTML pages in place to test functionality of basic links to pages and some simple error handling.

-----------Purpose of files-----------

All of the .html, .css, and .js files in the templates folder are currently for webpage design

routes.py - These are various functions based in Flask to handle various page routes and can be expanded upon as needed. There is a route for index.html as well as a dynamic route to allow routing to any template that is specified without creating a route for each page.

config.py - This is the initial setup before the server goes live. Once run.py is executed, this code will run before the server is live.

\_\_init__.py - This is the initialization code that creates our Flask app and will import anythink into the app as needed

run.py - This is the file that you will execute in the terminal to run the app. 'use_reloader=False' ensures that the page will not be reloaded as code is changed. This setting was placed due to issues in the app restarting and then freezing potentially due to changing variables in code
