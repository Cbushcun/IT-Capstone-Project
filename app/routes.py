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
        return render_template('index.html', previous_url=request.referrer, active_page='Home')
    

@app.route('/auction_page')
def auction_page():
    current_user = get_current_user()
    auctions = [
        {'auction_id': 1, 'seller_name': 'Alice', 'item_title': 'Vintage Lamp', 'end_time': '2023-10-15 12:00:00', 'buy_now_price': 50.00},
        {'auction_id': 2, 'seller_name': 'Bob', 'item_title': 'Antique Vase', 'end_time': '2023-10-18 15:30:00', 'buy_now_price': 120.00},
        # Add more filler data as needed
    ]
    if current_user:  
        
        return render_template('auction_page.html', active_page='Auctions', previous_url=request.referrer, current_user=current_user, auctions=auctions)
    else :
        return render_template('auction_page.html', previous_url=request.referrer, active_page='Auctions', auctions=auctions)
    

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

@app.route('/item/<int:item_id>')
def item_page(item_id):
    current_user = get_current_user()
    # Retrieve the item from the database using item_id
    # This is just an example; you need to replace it with actual database retrieval code
    item = {
        'item_id': 1,
        'seller_name': 'Alice',
        'item_title': 'Vintage Lamp',
        'end_time': '2023-10-15 12:00:00',
        'buy_now_price': 50.00,
        'description': 'A beautiful vintage lamp in excellent condition.',
        'image_filename': 'vintage_lamp.jpg'  # Example image filename; replace with actual filename
    }
    if current_user:      
        return render_template('item_page.html', active_page='Listing', previous_url=request.referrer, current_user=current_user, item=item)
    else :
        return render_template('item_page.html', previous_url=request.referrer, active_page='Listing', item=item)
    
@app.route('/user_profile')
def user_profile():
    user_id = session.get('user_id')
    user_data = fetch_user_from_database(user_id)
    current_user=get_current_user()
    if user_data:
        User = namedtuple('User', ['user_id', 'username', 'email', 'password', 'first_name', 'last_name', 'address', 'phone_number'])
        user = User(*user_data)
        if current_user:      
            return render_template('user_profile.html', active_page='Profile', previous_url=request.referrer, current_user=current_user, user=user)
        else :
            return render_template('user_profile.html', previous_url=request.referrer, active_page='Profile')
    else:
        # Handle the case where there is no user data
        return "User not found", 404