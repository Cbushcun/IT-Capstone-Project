from flask import Flask, request, render_template
from werkzeug.exceptions import BadRequest, Forbidden, NotFound, InternalServerError, MethodNotAllowed
from jinja2 import TemplateNotFound
from app import app
from config import *

#Routes to handle page navigation
@app.route('/')
def index():
    #current_user = get_current_user()  # You need to implement get_current_user()
    return render_template('index.html', active_page='Home', previous_url=request.referrer, #current_user=current_user
                           )

@app.route('/auction_page')
def auction_page():
    return render_template('auction_page.html', previous_url=request.referrer, active_page='Auction Listings')

@app.route('/login')
def login():
    registered = None
    return render_template('login.html', previous_url=request.referrer, active_page='Login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None # Initialize error as None
    if request.method == 'POST':        
        password = request.form.get('password')
        verify_password = request.form.get('verify_password')
        
        #Confirm that passwords match
        if password != verify_password:
            error = "Passwords do not match"
        else:
            error = register_user()

        if not error:
            registered = 'Registration Success!'
            return render_template('login.html', registered=registered)
    return render_template('register.html', previous_url=request.referrer, active_page='Register', error=error)

@app.route('/about_us')
def about():
    return render_template('about_us.html', previous_url=request.referrer, active_page='About Us')

@app.route('/contact_us')
def contact():
    return render_template('contact_us.html', previous_url=request.referrer, active_page='Contact Us')


# Routes to handle error handling
@app.errorhandler(BadRequest)
def handle_bad_request(e):
    logger.error(f"IP: {request.remote_addr} - Bad Request Error - Route: {request.path}")
    return render_template('400.html', error=e), 400

@app.errorhandler(Forbidden)
def handle_forbidden(e):
    logger.error(f"IP: {request.remote_addr} - Forbidden Error - Route: {request.path}")
    return render_template('403.html', error=e), 403

@app.errorhandler(NotFound)
@app.errorhandler(TemplateNotFound)
def handle_not_found(e):
    logger.error(f"IP: {request.remote_addr} - Not Found Error - Route: {request.path}")
    return render_template('404.html', error=e), 404

@app.errorhandler(MethodNotAllowed)
def handle_method_not_allowed(e):
    logger.error(f"IP: {request.remote_addr} - Method Not Allowed Error - Route: {request.path}")
    return render_template('405.html', error=e), 405

@app.errorhandler(InternalServerError)
def handle_internal_server_error(e):
    logger.error(f"IP: {request.remote_addr} - Internal Server Error - Route: {request.path}")
    return render_template('500.html', error=e), 500

@app.errorhandler(Exception)
def handle_exception(e):
    # Pass the error to handle_exception
    return render_template('error.html', error=str(e)), 500

