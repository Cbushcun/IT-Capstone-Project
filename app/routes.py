from flask import Flask, request, render_template, flash, get_flashed_messages
from werkzeug.exceptions import BadRequest, Forbidden, NotFound, InternalServerError, MethodNotAllowed
from jinja2 import TemplateNotFound
from app import app
from config import *

address = "http://127.0.0.1:5000" #to use in stripe route to handle payment success and cancel. Change when needed

#--------------------------------------------------------------------
#Sample data for testing purposes until complete database integration
#--------------------------------------------------------------------

user_bids_list = [
    {'auction_id': 1, 'seller_name': 'Alice', 'item_title': 'Vintage Lamp', 'end_time': '2023-10-15', 'buy_now_price': 50.00, 'current_bid': 35.00},
    {'auction_id': 2, 'seller_name': 'Bob', 'item_title': 'Antique Vase', 'end_time': '2023-10-18', 'buy_now_price': 120.00, 'current_bid': 80.00},
        # Add more filler data as needed
]

#--------------------------------
#Routes to handle page navigation
#--------------------------------

@app.route('/')
def index():
    current_user = session.get('username')
    if current_user is None:   
        return render_template('pages/index.html', active_page='Home') 
    else:
        return render_template('pages/index.html', active_page='Home', current_user=current_user)
        
@app.route('/auction_page')
def auction_page():
    current_user = session.get('username')

    # Pagination settings
    per_page = 25  # Number of listings per page
    page = request.args.get('page', type=int, default=1)

    # Calculate the start and end indices for the listings to display
    start = (page - 1) * per_page
    end = start + per_page

    available_auctions = get_unexpired_auctions()
    # Slice the auctions list to display only the relevant listings
    paginated_auctions = available_auctions[start:end]

    # Calculate the total number of pages
    total_pages = (len(available_auctions) + per_page - 1) // per_page

    if current_user is None:
        return render_template('pages/auction_page.html',active_page='Auctions',auctions=paginated_auctions,total_pages=total_pages,current_page=page)
    else :
        return render_template('pages/auction_page.html', active_page='Auctions', current_user=current_user, auctions=paginated_auctions,total_pages=total_pages,current_page=page)
    
# Route for viewing items in a specific auction
@app.route('/item/<int:auction_id>', methods=['GET', 'POST'])
def item_page(auction_id):
    current_user = session.get('username')

    # Find the relevant auction in the sample data based on auction_id
    item = find_auction_by_id(auction_id)
    seller_id = item[1]
    seller_info = fetch_user_from_database(seller_id)
    seller_name = seller_info[1]
    if request.method == 'POST':
        # Handle the bid submission
        new_bid = float(request.form['bid-amount'])
        
        if new_bid > item[6]:
            update_reserve_price(auction_id, new_bid)
        else:
            flash('Bid must be higher than the current bid', 'error')
            return redirect(url_for('item_page', auction_id=auction_id))

        # After updating the bid, redirect back to the item page to display the updated bid
        return redirect(url_for('item_page', auction_id=auction_id))
    
    if item is not None:
        # Pass the auctions list to the item_page route
        bid_finished = has_bid_ended(item)
        print("Bid finished: ", bid_finished) 

        if current_user is None:
            return render_template('pages/item_page.html', active_page='Listing', item=item, seller=seller_name)
        else:
            return render_template('pages/item_page.html', active_page='Listing', current_user=current_user, item=find_auction_by_id(auction_id), bid_finished=bid_finished, seller=seller_name)
            
    else:
        # Handle the case where the auction_id doesn't match any auction
        return "Item not found", 404

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = None
    print("DEBUG: Message initialized to None, should render login.html") #For Debugging
    if request.method == 'POST':
        print("DEBUG: Post method called") #For Debugging
        result = login_user()
        print("DEBUG: login_user() called and stored to 'result' variable ") #For Debugging
        
        if result is None: 
            print("DEBUG: Result is 'None', redirection to index") #For Debugging
            return redirect(url_for('index'))          
        else:
            print("DEBUG: Result is other than None, flashing error result from Login_user()") #For Debugging
            flash(result, "error")
            
    # Clear any existing flashed messages
    get_flashed_messages(category_filter=["error"]) 
    return render_template('pages/login.html', active_page='Login', error=message)

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
                return redirect(url_for('login'))
    return render_template('pages/register.html', active_page='Register', error=error)

@app.route('/about_us')
def about():
    current_user = session.get('username')

    if current_user is None:
        return render_template('about_us.html', active_page='About Us')
    else :
        return render_template('about_us.html', active_page='About Us', current_user=current_user)
        
    
@app.route('/contact_us')
def contact():
    current_user = session.get('username')
    if current_user is None:      
        return render_template('contact_us.html', active_page='Contact Us') 
    else:
        return render_template('contact_us.html', active_page='Contact Us', current_user=current_user)

@app.route('/payment_cancel')
def payment_cancel():
    current_user = session.get('username')
    if current_user is None:   
        return render_template('payment_cancel.html', active_page='Home') 
    else:
        return render_template('payment_cancel.html', active_page='Home', current_user=current_user)

@app.route('/payment_success')
def payment_success():
    current_user = session.get('username')
    if current_user is None:   
        return render_template('payment_success.html', active_page='Home') 
    else:
        return render_template('payment_success.html', active_page='Home', current_user=current_user)

@app.route('/create-checkout-session')
def create_checkout_session():
    item_price = float(request.args.get('price'))  # Default price if not provided

    # Create a Stripe Checkout Session with the dynamic item price
    stripe_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'Your Product Name',
                },
                'unit_amount': int(item_price * 100),
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=address + "/payment_success",
        cancel_url=address + "/payment_cancel"
    )

    return jsonify({'sessionId': stripe_session.id})

#-------------------------------
#Routes only for logged in users
#-------------------------------

@app.route('/user_profile')
def user_profile():
    user_id = session.get('user_id')
    user_data = fetch_user_from_database(user_id)
    current_user=get_current_user()
    if user_data:
        User = namedtuple('User', ['user_id', 'username', 'email', 'password', 'first_name', 'last_name', 'address', 'phone_number'])
        user = User(*user_data)
        if current_user is None:      
            return render_template('user_pages/user_profile.html', active_page='Profile')
        else :
            return render_template('user_pages/user_profile.html', active_page='Profile', current_user=current_user, user=user)
            
    else:
        # Handle the case where there is no user data
        return redirect(url_for('login'))
    
@app.route('/create_auction', methods=['GET', 'POST'])
def create_auction():
    user_id = session.get('user_id')
    current_user=get_current_user()

    if request.method == 'POST':
        print("post method called") #for debugging

        # Get form data from the request
        title = request.form['title']
        description = request.form['description']
        end_time = request.form['end_time']
        starting_bid = float(request.form['reserve_price'])  # Convert to float
        start_time = datetime.datetime.now().date()
        print("data retrieved") #for debugging

        create_auction_in_database( user_id, title, description, start_time, end_time, starting_bid)
        # Create a new auction object
        print("auction row created") #for debugging
        
        # You can optionally redirect to a page showing the newly created auction
        return redirect(url_for('item_page', auction_id=get_most_recent_auction_id()))
    
    if current_user is None:      
        return redirect(url_for('login'))
    else:
        return render_template('user_pages/create_auction.html', active_page='List an Item', current_user=current_user)
    
@app.route('/user_bids_page')
def user_bids_page():
    current_user = session.get('username')

    # Pagination settings
    per_page = 25  # Number of listings per page
    page = request.args.get('page', type=int, default=1)

    # Calculate the start and end indices for the listings to display
    start = (page - 1) * per_page
    end = start + per_page

    completed_bids = find_completed_auctions(user_bids_list)
    # Slice the user_bids_list to display only the relevant listings
    paginated_bids = completed_bids[start:end]

    # Calculate the total number of pages
    total_pages = (len(user_bids_list) + per_page - 1) // per_page

    if current_user is None: 
        return redirect(url_for('login')) 
    else:
        return render_template('user_pages/user_bids.html', active_page='Your Bids', current_user=current_user, bids=paginated_bids, total_pages=total_pages, current_page=page)
    
#-------------------------------
#Routes to handle error handling
#-------------------------------

@app.errorhandler(BadRequest)
def handle_bad_request(e):
    log_data()
    return render_template('errors/400.html', error=e), 400

@app.errorhandler(Forbidden)
def handle_forbidden(e):
    log_data()
    return render_template('errors/403.html', error=e), 403

@app.errorhandler(NotFound)
@app.errorhandler(TemplateNotFound)
def handle_not_found(e):
    log_data()
    return render_template('errors/404.html', error=e), 404

@app.errorhandler(MethodNotAllowed)
def handle_method_not_allowed(e):
    log_data()
    return render_template('errors/405.html', error=e), 405

@app.errorhandler(InternalServerError)
def handle_internal_server_error(e):
    log_data()
    return render_template('errors/500.html', error=e), 500

@app.errorhandler(Exception)
def handle_exception(e):
    # Pass the error to handle_exception
    return render_template('errors/error.html', error=str(e)), 500