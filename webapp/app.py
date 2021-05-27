from flask import Flask, jsonify, request
from utils import load_models
from preprocessing import Preprocessing_Pipeline
import pandas as pd

app = Flask(__name__)
lgbm_pipe, rf_pipe = load_models()

@app.route('/predict', methods=['POST','GET'])
def make_prediction():
    if request.method == 'GET':
        return jsonify({"message":"Submit your prediction in JSON format"})

    elif request.method == 'POST':

        data = request.json #es un dict
        #Validar datos.
        
        #Pipeline
        dataframe = Preprocessing_Pipeline(data_dict = data).transform()
        
        #Prediction
        prediction = lgbm_pipe.predict(dataframe)
        #Como los arrays no son jsonifybles:
        prediction = pd.Series(prediction).to_json(orient='values')

        return jsonify({'message':'Se logro?', 'prediccion': prediction})

    return jsonify({'message':'does not Found'})

if __name__ == "__main__":
    app.run(debug=True, port = 420)