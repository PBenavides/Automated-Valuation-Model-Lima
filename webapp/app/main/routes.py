from flask import render_template
from app.main import bp

@bp.route('/')
def main():
    return render_template('home.html')

@bp.route('/contact')
def contact():
    return render_template('contact.html')