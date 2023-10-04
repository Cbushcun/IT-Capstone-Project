from flask import request, render_template
from jinja2 import TemplateNotFound
from werkzeug.exceptions import BadRequest, Forbidden, NotFound, InternalServerError, MethodNotAllowed
from app import app
from config import *
import logging
from datetime import datetime

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
    return render_template('login.html', previous_url=request.referrer, active_page='Login')

@app.route('/register')
def register():
    return render_template('register.html', previous_url=request.referrer, active_page='Register')  

@app.route('/about_us')
def about():
    return render_template('about_us.html', previous_url=request.referrer, active_page='About Us')

@app.route('/contact_us')
def contact():
    return render_template('contact_us.html', previous_url=request.referrer, active_page='Contact Us')


# Routes to handle error handling
@app.errorhandler(BadRequest)
def handle_bad_request(e):
    logging.error(f"Bad Request Error: {e.description} - Route: {request.path} - IP: {request.remote_addr}")
    return render_template('400.html', error=e.description), 400

@app.errorhandler(Forbidden)
def handle_forbidden(e):
    logging.warning(f"Forbidden Error: {e.description} - Route: {request.path} - IP: {request.remote_addr}")
    return render_template('403.html', error=e.description), 403

@app.errorhandler(NotFound)
def handle_not_found(e):
    logging.info(f"Not Found Error: {e.description} - Route: {request.path} - IP: {request.remote_addr}")
    return render_template('404.html', error=e.description), 404

@app.errorhandler(MethodNotAllowed)
def handle_method_not_allowed(e):
    logging.warning(f"Method Not Allowed Error: {e.description} - Route: {request.path} - IP: {request.remote_addr}")
    return render_template('405.html', error=e.description), 405

@app.errorhandler(InternalServerError)
def handle_internal_server_error(e):
    logging.critical(f"Internal Server Error: {e.description} - Route: {request.path} - IP: {request.remote_addr}")
    return render_template('500.html', error=e.description), 500

