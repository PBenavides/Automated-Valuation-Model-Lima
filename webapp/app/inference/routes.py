from flask import render_template, jsonify, request, current_app
from app.inference.forms import ValuationForm
from app.inference import bp
from app.inference.preprocessing import Preprocessing_Pipeline

import pandas as pd
import time

@bp.route('/predict', methods=['POST','GET'])
def predict():

    form = ValuationForm(request.form)
    
    if form.validate_on_submit():
        current_app.logger.info('Form was submitted by: {}'.format(request.remote_addr))
        data = form.data #es un dict
        
        #current_app.logger.info('Ha sido recibida un request POST {}'.format(data))
        #Validar datos.
        print(data,'/n', type(data))
        #Pipeline
        dataframe = Preprocessing_Pipeline(data_dict = data).transform()
        
        lgbm_model = current_app.config['model_dict']['lgbm_base']
        rf_model = current_app.config['model_dict']['rf_base']

        #Prediction
        prediction_lgbm = lgbm_model.predict(dataframe)
        #Como los arrays no son jsonifybles:
        prediction_lgbm = pd.Series(prediction_lgbm).to_json(orient='values')

        prediction_rf = rf_model.predict(dataframe)
        prediction_rf = pd.Series(prediction_rf).to_json(orient='values')

        current_app.logger.info('lgbm-pred: {}'.format(prediction_lgbm))
        current_app.logger.info('rf-pred: {}'.format(prediction_rf))
        
        return render_template('success.html', prediction_lgbm = prediction_lgbm,\
            prediction_rf=prediction_rf)

    return render_template('predict.html', form = form)

@bp.route('/api-predict',methods=['POST','GET'])
def api_predict():

    if request.method == 'GET':
        return render_template('api-predict.html')

    elif request.method == 'POST':
        start = time.time()
        
        data = request.json #es un dict
        #current_app.logger.info('Ha sido recibida un request POST {}'.format(data))
        #Validar datos.
        
        lgbm_model = current_app.config.model_dict['lgbm_base']
        rf_model = current_app.config.model_dict['rf_base']

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