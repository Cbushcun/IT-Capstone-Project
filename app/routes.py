from flask import Flask, request, render_template, flash, get_flashed_messages
from werkzeug.exceptions import BadRequest, Forbidden, NotFound, InternalServerError, MethodNotAllowed
from jinja2 import TemplateNotFound
from app import app
from config import *

#Routes to handle page navigation
@app.route('/')
def index():
    current_user = get_current_user()
    if current_user:      
        return render_template('index.html', active_page='Home', previous_url=request.referrer, current_user=current_user)
    else :
        return render_template('index.html', active_page='Home', previous_url=request.referrer)
    

@app.route('/auction_page')
def auction_page():
    current_user = get_current_user()
    if current_user:      
        return render_template('auction_page.html', active_page='Auction Listings', previous_url=request.referrer, current_user=current_user)
    else :
        return render_template('auction_page.html', previous_url=request.referrer, active_page='Auction Listings')
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = None
    print("message initialized to None, should render login.html") #For Debugging
    if request.method == 'POST':
        print("Post method called") #For Debugging
        result = login_user()
        print("Login_user() called and stored to result") #For Debugging
        
        if result is None: 
            print("Result is 'None', redirection to index") #For Debugging
            return redirect(url_for('index'))          
        else:
            print("result is other than None, flashing error result from Login_user()") #For Debugging
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
    print("error = None initialized") #For Debugging
    if request.method == 'POST': 
        print("POST method called") #For Debugging
        password = request.form.get('password')
        print("Password stored") #For Debugging
        verify_password = request.form.get('verify_password')
        print("Confirmation password stored") #For Debugging
        
        #Confirm that passwords match
        if password != verify_password:
            flash("Passwords do no t match", "error")
            print("Password mismatch") #For Debugging
        else:
            error = register_user()
            print("Passwords match, storing user") #For Debugging

            if error:
                flash(error, "error")
            else:             
                flash('Registration Success!', 'success')
                print("Registration success flashed") #For Debugging      
                return redirect(url_for('login', active_page='Login'))
    return render_template('register.html', previous_url=request.referrer, active_page='Register', error=error)

@app.route('/about_us')
def about():
    current_user = get_current_user()
    if current_user:      
        return render_template('about_us.html', active_page='About Us', previous_url=request.referrer, current_user=current_user)
    else :
        return render_template('about_us.html', previous_url=request.referrer, active_page='About Us')
    

@app.route('/contact_us')
def contact():
    current_user = get_current_user()
    if current_user:      
        return render_template('contact_us.html', active_page='Contact Us', previous_url=request.referrer, current_user=current_user)
    else :
        return render_template('contact_us.html', previous_url=request.referrer, active_page='Contact Us')


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

