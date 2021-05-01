from flask import Flask, request


from predictor_api import make_prediction

app = Flask(__name__)

@app.route('/about')
def about():
    print("<h1> About </h1>")


@app.route('/',methods=['GET','POST'])
def predict():
    return 0

