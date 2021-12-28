from flask import Flask
from config import Config


app = Flask(__name__)
app.config.from_object(Config)
    #register blueprints..
    

print('APP create_ app, imported. ended')

from app import routes, forms