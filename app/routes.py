from flask import render_template, logging
from app import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<path:page_direction>')
def dynamic_page(page_direction):
    # 'page_direction' will contain the input from the URL
    return render_template(page_direction)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(Exception)
def handle_error(e):
    return render_template('error.html', error=e), 500

