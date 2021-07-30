from flask import Flask, render_template
#from flask_sqlalchemy import SQLAlchemy
from webpage.utils import load_models

app = Flask(__name__)
#app.config['SQALCHEMY_DATABASE_URI'] = 'sqlite:///valuations.db'
app.config['SECRET_KEY'] = 'llaveextremadamentesecreta'
#db = SQLAlchemy(app)
lgbm_model, rf_model = load_models()

from webpage import routes