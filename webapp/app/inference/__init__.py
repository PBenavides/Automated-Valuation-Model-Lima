from flask import Blueprint

bp = Blueprint('inference', __name__)

from app.inference import routes