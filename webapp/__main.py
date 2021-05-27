from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse
import pickle
import pandas as pd

app = Flask(__name__)
API = Api(app)

def load_models():
    with open('artifacts/models/lgbm.pkl','rb') as handle:
        lgbm_model = pickle.load(handle)

    with open('artifacts/models/random_forest.pkl','rb') as handle:
        rf_model = pickle.load(handle)
    return lgbm_model, rf_model

class Root(Resource):
    
    @staticmethod
    def get():
        message = {'version':'0.01',
                   'description': 'Automated Valuation Model API',
                   'instructions': 'go to /predict and post your request'
                   }

        return jsonify(message)

    @staticmethod
    def put():
        message = request.json
        return jsonify({'nuevo_mensaje': message})

class Predict(Resource):

    @staticmethod
    def post():

        parser = reqparse.RequestParser()
        parser.add_argument('first_arg')
        parser.add_argument('second_arg')

        lgbm_model, rf_model = load_models()

        args = parser.parse_args()

        #X_new = pd.Series(np.fromiter(args.values(), dtype=float))

        #out = {'Prediction_lgbm': lgbm_model.predict(X_new)}
        out = {'Mensaje Enviado': args.values()}

        return out, 200

    @staticmethod
    def get():
        message = {'version':'0.01',
                   'description': 'Automated Valuation Model API',
                   'input':'Input has to be dictionary type'}

        return jsonify(message)

API.add_resource(Root,'/')
API.add_resource(Predict, '/predict')

if __name__ == '__main__':
    app.run(debug=True, port='4020')
