from flask import Flask, request
from predictor_api import make_prediction

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def predict():
    return 0
