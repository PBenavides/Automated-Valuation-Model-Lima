from flask import Flask, jsonify, request, current_app, render_template
from utils import load_models
from preprocessing import Preprocessing_Pipeline
import pandas as pd

app = Flask(__name__)
lgbm_model, rf_model = load_models()

@app.route('/')
def main():
    text= {'welcome_message': 'Hola! Bienvenido a la API de Valuación de casas'}
    return render_template('index.html',title='House Pricing Lima - ', text=text)

@app.route('/predict', methods=['POST','GET'])
def make_prediction():
    if request.method == 'GET':
        return jsonify({"message":"Submit your prediction in JSON format"})

    elif request.method == 'POST':
        #LOG
        
        data = request.json #es un dict
        current_app.logger.info('Ha sido recibida un request POST {}'.format(data))
        #Validar datos.
        
        #Pipeline
        dataframe = Preprocessing_Pipeline(data_dict = data).transform()
        
        #Prediction
        prediction_lgbm = lgbm_model.predict(dataframe)
        #Como los arrays no son jsonifybles:
        prediction_lgbm = pd.Series(prediction_lgbm).to_json(orient='values')

        prediction_rf = rf_model.predict(dataframe)
        prediction_rf = pd.Series(prediction_rf).to_json(orient='values')

        return jsonify({'message':'Precio por m2 cotizado:',\
                'prediccion_lgbm': prediction_lgbm, 'prediccion_rf': prediction_rf})

    return jsonify({'message':'does not Found'})

if __name__ == "__main__":
    app.run(debug=True, port = 420)