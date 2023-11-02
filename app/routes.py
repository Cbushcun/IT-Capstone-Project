from flask import Flask, request, render_template, flash, get_flashed_messages
from werkzeug.exceptions import BadRequest, Forbidden, NotFound, InternalServerError, MethodNotAllowed
from jinja2 import TemplateNotFound
from app import app
from config import *


#--------------------------------------------------------------------
#Sample data for testing purposes until complete database integration
#--------------------------------------------------------------------

auctions = [
    {'auction_id': 1, 'seller_name': 'Alice', 'item_title': 'Vintage Lamp', 'end_time': '2023-10-15', 'buy_now_price': 50.00, 'current_bid': 35.00},
    {'auction_id': 2, 'seller_name': 'Bob', 'item_title': 'Antique Vase', 'end_time': '2023-10-18', 'buy_now_price': 120.00, 'current_bid': 80.00},
    {'auction_id': 3, 'seller_name': 'Charlie', 'item_title': 'Rare Collectible Coin', 'end_time': '2023-10-20', 'buy_now_price': 75.50, 'current_bid': 60.00},
    {'auction_id': 4, 'seller_name': 'David', 'item_title': 'Art Deco Mirror', 'end_time': '2023-10-22', 'buy_now_price': 90.00, 'current_bid': 70.00},
    {'auction_id': 5, 'seller_name': 'Eve', 'item_title': 'Vintage Typewriter', 'end_time': '2023-10-25', 'buy_now_price': 60.00, 'current_bid': 45.00},
    {'auction_id': 6, 'seller_name': 'Frank', 'item_title': 'Rare Stamp Collection', 'end_time': '2023-10-28', 'buy_now_price': 110.00, 'current_bid': 95.00},
    {'auction_id': 7, 'seller_name': 'Grace', 'item_title': 'Vintage Record Player', 'end_time': '2023-10-30', 'buy_now_price': 70.00, 'current_bid': 55.00},
    {'auction_id': 8, 'seller_name': 'Henry', 'item_title': 'Antique Clock', 'end_time': '2023-11-02', 'buy_now_price': 85.00, 'current_bid': 65.00},
    {'auction_id': 9, 'seller_name': 'Ivy', 'item_title': 'Classic Film Poster', 'end_time': '2023-11-05', 'buy_now_price': 55.00, 'current_bid': 40.00},
    {'auction_id': 10, 'seller_name': 'Jack', 'item_title': 'Rare Baseball Card', 'end_time': '2023-11-08', 'buy_now_price': 150.00, 'current_bid': 120.00},
    {'auction_id': 11, 'seller_name': 'Karen', 'item_title': 'Vintage Guitar', 'end_time': '2023-11-10', 'buy_now_price': 180.00, 'current_bid': 140.00},
    {'auction_id': 12, 'seller_name': 'Larry', 'item_title': 'Collectible Comics', 'end_time': '2023-11-12', 'buy_now_price': 70.00, 'current_bid': 50.00},
    {'auction_id': 13, 'seller_name': 'Megan', 'item_title': 'Rare Stamps', 'end_time': '2023-11-15', 'buy_now_price': 65.00, 'current_bid': 55.00},
    {'auction_id': 14, 'seller_name': 'Nina', 'item_title': 'Vintage Camera', 'end_time': '2023-11-18', 'buy_now_price': 95.00, 'current_bid': 70.00},
    {'auction_id': 15, 'seller_name': 'Oscar', 'item_title': 'Antique Jewelry', 'end_time': '2023-11-20', 'buy_now_price': 120.00, 'current_bid': 100.00},
    {'auction_id': 16, 'seller_name': 'Paul', 'item_title': 'Classic Coins', 'end_time': '2023-11-22', 'buy_now_price': 55.00, 'current_bid': 40.00},
    {'auction_id': 17, 'seller_name': 'Quincy', 'item_title': 'Vintage Art', 'end_time': '2023-11-25', 'buy_now_price': 70.00, 'current_bid': 50.00},
    {'auction_id': 18, 'seller_name': 'Rachel', 'item_title': 'Rare Watches', 'end_time': '2023-11-28', 'buy_now_price': 110.00, 'current_bid': 85.00},
    {'auction_id': 19, 'seller_name': 'Sam', 'item_title': 'Antique Furniture', 'end_time': '2023-11-30', 'buy_now_price': 200.00, 'current_bid': 150.00},
    {'auction_id': 20, 'seller_name': 'Tom', 'item_title': 'Vintage Books', 'end_time': '2023-12-02', 'buy_now_price': 45.00, 'current_bid': 30.00},
    {'auction_id': 21, 'seller_name': 'Ursula', 'item_title': 'Collectible Toys', 'end_time': '2023-12-05', 'buy_now_price': 80.00, 'current_bid': 60.00},
    {'auction_id': 22, 'seller_name': 'Victor', 'item_title': 'Classic Paintings', 'end_time': '2023-12-08', 'buy_now_price': 150.00, 'current_bid': 120.00},
    {'auction_id': 23, 'seller_name': 'Wendy', 'item_title': 'Rare Sculptures', 'end_time': '2023-12-10', 'buy_now_price': 130.00, 'current_bid': 100.00},
    {'auction_id': 24, 'seller_name': 'Xander', 'item_title': 'Vintage Maps', 'end_time': '2023-12-12', 'buy_now_price': 60.00, 'current_bid': 45.00},
    {'auction_id': 25, 'seller_name': 'Yvonne', 'item_title': 'Antique Pottery', 'end_time': '2023-12-15', 'buy_now_price': 75.00, 'current_bid': 60.00},
    {'auction_id': 26, 'seller_name': 'Zane', 'item_title': 'Classic Coins', 'end_time': '2023-12-18', 'buy_now_price': 55.00, 'current_bid': 40.00},
    {'auction_id': 27, 'seller_name': 'Amy', 'item_title': 'Vintage Jewelry', 'end_time': '2023-12-20', 'buy_now_price': 90.00, 'current_bid': 70.00},
    {'auction_id': 28, 'seller_name': 'Ben', 'item_title': 'Rare Watches', 'end_time': '2023-12-22', 'buy_now_price': 110.00, 'current_bid': 85.00},
    {'auction_id': 29, 'seller_name': 'Cathy', 'item_title': 'Antique Furniture', 'end_time': '2023-12-25', 'buy_now_price': 200.00, 'current_bid': 150.00},
    {'auction_id': 30, 'seller_name': 'Dan', 'item_title': 'Vintage Books', 'end_time': '2023-12-28', 'buy_now_price': 45.00, 'current_bid': 30.00},
    {'auction_id': 31, 'seller_name': 'Ella', 'item_title': 'Collectible Toys', 'end_time': '2023-12-30', 'buy_now_price': 80.00, 'current_bid': 60.00},
    {'auction_id': 32, 'seller_name': 'Fred', 'item_title': 'Classic Paintings', 'end_time': '2024-01-02', 'buy_now_price': 150.00, 'current_bid': 100.00},
    {'auction_id': 33, 'seller_name': 'Gina', 'item_title': 'Rare Sculptures', 'end_time': '2024-01-05', 'buy_now_price': 130.00, 'current_bid': 90.00},
    {'auction_id': 34, 'seller_name': 'Hank', 'item_title': 'Vintage Maps', 'end_time': '2024-01-08', 'buy_now_price': 60.00, 'current_bid': 40.00},
    {'auction_id': 35, 'seller_name': 'Isabel', 'item_title': 'Antique Pottery', 'end_time': '2024-01-10', 'buy_now_price': 75.00, 'current_bid': 60.00},
    {'auction_id': 36, 'seller_name': 'Jake', 'item_title': 'Classic Coins', 'end_time': '2024-01-12', 'buy_now_price': 55.00, 'current_bid': 40.00},
    {'auction_id': 37, 'seller_name': 'Karen', 'item_title': 'Vintage Jewelry', 'end_time': '2024-01-15', 'buy_now_price': 90.00, 'current_bid': 70.00},
    {'auction_id': 38, 'seller_name': 'Larry', 'item_title': 'Rare Watches', 'end_time': '2024-01-18', 'buy_now_price': 110.00, 'current_bid': 85.00},
    {'auction_id': 39, 'seller_name': 'Megan', 'item_title': 'Antique Furniture', 'end_time': '2024-01-20', 'buy_now_price': 200.00, 'current_bid': 150.00},
    {'auction_id': 40, 'seller_name': 'Nina', 'item_title': 'Vintage Books', 'end_time': '2024-01-22', 'buy_now_price': 45.00, 'current_bid': 30.00},
    {'auction_id': 41, 'seller_name': 'Oscar', 'item_title': 'Collectible Toys', 'end_time': '2024-01-25', 'buy_now_price': 80.00, 'current_bid': 60.00},
    {'auction_id': 42, 'seller_name': 'Paul', 'item_title': 'Classic Paintings', 'end_time': '2024-01-28', 'buy_now_price': 150.00, 'current_bid': 100.00},
    {'auction_id': 43, 'seller_name': 'Quincy', 'item_title': 'Rare Sculptures', 'end_time': '2024-01-30', 'buy_now_price': 130.00, 'current_bid': 100.00},
    {'auction_id': 44, 'seller_name': 'Rachel', 'item_title': 'Vintage Maps', 'end_time': '2024-02-02', 'buy_now_price': 60.00, 'current_bid': 100.00},
    {'auction_id': 45, 'seller_name': 'Sam', 'item_title': 'Antique Pottery', 'end_time': '2024-02-05', 'buy_now_price': 75.00, 'current_bid': 100.00},
    {'auction_id': 46, 'seller_name': 'Tom', 'item_title': 'Classic Coins', 'end_time': '2024-02-08', 'buy_now_price': 55.00, 'current_bid': 100.00},
    {'auction_id': 47, 'seller_name': 'Ursula', 'item_title': 'Vintage Jewelry', 'end_time': '2024-02-10', 'buy_now_price': 90.00, 'current_bid': 100.00},
    {'auction_id': 48, 'seller_name': 'Victor', 'item_title': 'Rare Watches', 'end_time': '2024-02-12', 'buy_now_price': 110.00, 'current_bid': 100.00},
    {'auction_id': 49, 'seller_name': 'Wendy', 'item_title': 'Antique Furniture', 'end_time': '2024-02-15', 'buy_now_price': 200.00, 'current_bid': 100.00},
    {'auction_id': 50, 'seller_name': 'Xander', 'item_title': 'Vintage Books', 'end_time': '2024-02-18', 'buy_now_price': 45.00, 'current_bid': 100.00},
]

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

    # Slice the auctions list to display only the relevant listings
    paginated_auctions = auctions[start:end]

    # Calculate the total number of pages
    total_pages = (len(auctions) + per_page - 1) // per_page

    if current_user is None:
        return render_template('pages/auction_page.html',active_page='Auctions',auctions=paginated_auctions,total_pages=total_pages,current_page=page)
    else :
        return render_template('pages/auction_page.html', active_page='Auctions', current_user=current_user, auctions=paginated_auctions,total_pages=total_pages,current_page=page)
    
# Route for viewing items in a specific auction
@app.route('/item/<int:auction_id>', methods=['GET', 'POST'])
def item_page(auction_id):
    current_user = session.get('username')

    # Find the relevant auction in the sample data based on auction_id
    item = next((auction for auction in auctions if auction['auction_id'] == auction_id), None)

    if request.method == 'POST':
        # Handle the bid submission
        new_bid = float(request.form['bid-amount'])
        if new_bid > item['current_bid']:
            item['current_bid'] = new_bid
        else:
            flash('Bid must be higher than the current bid', 'error')
            return redirect(url_for('item_page', auction_id=auction_id))

        # After updating the bid, redirect back to the item page to display the updated bid
        return redirect(url_for('item_page', auction_id=auction_id))
    
    if item is not None:
        # Pass the auctions list to the item_page route
        item['auctions'] = auctions

        if current_user is None:
            return render_template('pages/item_page.html', active_page='Listing', item=item)
        else:
            return render_template('pages/item_page.html', active_page='Listing', current_user=current_user, item=item)
            
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
        reserve_price = float(request.form['reserve_price'])  # Convert to float
        starting_bid = float(request.form['starting_bid'])  # Convert to float
        print("data retrieved") #for debugging

        # Create a new auction object
        auction = {
            'seller_name': session.get('username'),
            'auction_id': len(auctions) + 1,
            'item_title': title,
            'description': description,
            'end_time': end_time,
            'buy_now_price': reserve_price,
            'current_bid': starting_bid,
        }
        print("auction object created") #for debugging

        # Append the auction to the 'auctions' list
        auctions.append(auction)
        print("Auction appdended") #for debugging

        # You can optionally redirect to a page showing the newly created auction
        return redirect(url_for('item_page', auction_id=len(auctions)))
    
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