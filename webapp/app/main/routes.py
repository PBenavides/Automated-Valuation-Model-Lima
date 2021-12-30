from werkzeug.local import LocalProxy
from flask import render_template, current_app, request
from app.main import bp

logger = LocalProxy(lambda: current_app.logger)

@bp.route('/')
def main():
    
    logger.info('IP: {} enter home'.format(request.remote_addr))

    return render_template('home.html')

@bp.route('/contact')
def contact():
    logger.info('IP: {} enter contact'.format(request.remote_addr))
    return render_template('contact.html')