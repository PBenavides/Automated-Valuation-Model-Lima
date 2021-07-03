from webpage.forms import ValuationForm
from webpage import app, lgbm_model, rf_model
from flask import render_template, request, jsonify
from webpage.preprocessing import Preprocessing_Pipeline
from webpage.utils import load_models
import pandas as pd
import time

@app.route('/')
def main():
    return render_template('home.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/predict', methods=['POST','GET'])
def predict():

    form = ValuationForm(request.form)

    if form.validate_on_submit():

        data = form.data #es un dict
        
        #current_app.logger.info('Ha sido recibida un request POST {}'.format(data))
        #Validar datos.
        print(data,'/n', type(data))
        #Pipeline
        dataframe = Preprocessing_Pipeline(data_dict = data).transform()
        
        #Prediction
        prediction_lgbm = lgbm_model.predict(dataframe)
        #Como los arrays no son jsonifybles:
        prediction_lgbm = pd.Series(prediction_lgbm).to_json(orient='values')

        prediction_rf = rf_model.predict(dataframe)
        prediction_rf = pd.Series(prediction_rf).to_json(orient='values')

        return render_template('success.html', prediction_lgbm = prediction_lgbm[0], prediction_rf=prediction_rf[0])
    else:
        return render_template('predict.html', form = form)

@app.route('/api-predict',methods=['POST','GET'])
def api_predict():

    if request.method == 'GET':
        return render_template('api-predict.html')

    elif request.method == 'POST':
        start = time.time()
        
        data = request.json #es un dict
        #current_app.logger.info('Ha sido recibida un request POST {}'.format(data))
        #Validar datos.
        
        #Pipeline
        dataframe = Preprocessing_Pipeline(data_dict = data).transform()
        
        #Prediction
        prediction_lgbm = lgbm_model.predict(dataframe)

        #Como los arrays no son jsonifybles:
        prediction_lgbm = pd.Series(prediction_lgbm).to_json(orient='values')

        prediction_rf = rf_model.predict(dataframe)
        prediction_rf = pd.Series(prediction_rf).to_json(orient='values')

        end = time.time()
        print('TIME: ', end - start)
        return jsonify({'message':'Precio por m2 cotizado:',\
                'prediccion_lgbm': prediction_lgbm, 'prediccion_rf': prediction_rf})

    return jsonify({'message':'does not Found'})