from flask import Flask, request, render_template, flash, get_flashed_messages
from werkzeug.exceptions import BadRequest, Forbidden, NotFound, InternalServerError, MethodNotAllowed
from jinja2 import TemplateNotFound
from app import app
from config import *

#Routes to handle page navigation
@app.route('/')
def index():
    return routes_render_template('index.html', 'Home')
    

@app.route('/auction_page')
def auction_page():
    return routes_render_template('auction_page.html', 'Auctions Page')
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = None
    print("DEBUG: Message initialized to None, should render login.html") #For Debugging
    if request.method == 'POST':
        print("DEBUG: Post method called") #For Debugging
        result = login_user()
        print("DEBUG: login_user() called and stored to result") #For Debugging
        
        if result is None: 
            print("DEBUG: Result is 'None', redirection to index") #For Debugging
            return redirect(url_for('index'))          
        else:
            print("DEBUG: Result is other than None, flashing error result from Login_user()") #For Debugging
            flash(result, "error")
    # Clear any existing flashed messages
    get_flashed_messages(category_filter=["error"]) 
    return render_template('login.html', previous_url=request.referrer, active_page='Login', error=message)

@app.route('/logout')
def logout():
    return logout_user()

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None # Initialize error as None
    print("DEBUG: error = None initialized") #For Debugging
    if request.method == 'POST': 
        print("DEBUG: POST method called") #For Debugging
        password = request.form.get('password')
        print("DEBUG: Password stored") #For Debugging
        verify_password = request.form.get('verify_password')
        print("DEBUG: Confirmation password stored") #For Debugging
        
        #Confirm that passwords match
        if password != verify_password:
            flash("Passwords do no t match", "error")
            print("DEBUG: Password mismatch") #For Debugging
        else:
            error = register_user()
            print("DEBUG: Passwords match, storing user") #For Debugging

            if error:
                flash(error, "error")
            else:             
                flash('Registration Success!', 'success')
                print("DEBUG: Registration success flashed") #For Debugging      
                return redirect(url_for('login', active_page='Login'))
    return render_template('register.html', previous_url=request.referrer, active_page='Register', error=error)

@app.route('/about_us')
def about():
    return routes_render_template('about_us.html', 'About Us')
    

@app.route('/contact_us')
def contact():
    return routes_render_template('contact_us.html', 'Contact Us')


# Routes to handle error handling
@app.errorhandler(BadRequest)
def handle_bad_request(e):
    log_data()
    return render_template('400.html', error=e), 400

@app.errorhandler(Forbidden)
def handle_forbidden(e):
    log_data()
    return render_template('403.html', error=e), 403

@app.errorhandler(NotFound)
@app.errorhandler(TemplateNotFound)
def handle_not_found(e):
    log_data()
    return render_template('404.html', error=e), 404

@app.errorhandler(MethodNotAllowed)
def handle_method_not_allowed(e):
    log_data()
    return render_template('405.html', error=e), 405

@app.errorhandler(InternalServerError)
def handle_internal_server_error(e):
    log_data()
    return render_template('500.html', error=e), 500

@app.errorhandler(Exception)
def handle_exception(e):
    # Pass the error to handle_exception
    return render_template('error.html', error=str(e)), 500

