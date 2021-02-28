import pandas as pd 
import numpy as np 
from data import Data_MlApproach
from create_folds import make_training_dataframe
from utils import subdict_metrics




import pickle

class TimeSeriesTrainer():
    """
    This class will serve to train different models with multiple parameters.
    Also, to store the results with loggs.
    """
    def __init__(self, model, params):
        self.model = model
        self.params = params

        self.predictions_dict = {}
        self.original_values_dict = {}
        
        self.dict_districts_preds = {} 
        self.dict_districts_actuals = {}

        self.dict_districs_metrics = {district: [] for district in Data_MlApproach().prototyping_districts}
        self.to_train = pd.read_csv('./input/preprocess_data/to_train.csv')


    def train_and_test_data(self):
        
        #Importing dict_encoders.
        
        with open('./models/objects/dict_encoders.pickle','rb') as handle:
                dict_encoders = pickle.load(handle)

        for n in range(60, len(self.to_train['Fecha'].unique()[:-5])):

            training_data, testing_data, testing_date = make_training_dataframe(self.to_train, window_size=n)
            
            ##                              COMO IMPORTAR PARAMS DESDE EL DISPATCHER?
            ##
            regression_model = self.model(params = self.params)

            X_train, y_train = training_data.drop('target',axis=1), training_data['target']
            X_test, y_test = testing_data.drop('target',axis=1), testing_data['target']

            regression_model.fit(X_train, y_train)
            predictions = regression_model.predict(X_test)

            #For the total:
            self.predictions_dict[testing_date] = predictions #Predictions

            self.original_values_dict[testing_date] = y_test #Actuals

            X_test['predictions'] = predictions
            X_test['actuals'] = y_test

            data_distritos_preds = X_test.groupby('Distrito')[['predictions']].agg('median').reset_index()
            #Calling inverse encoding on Districts.
            data_distritos_preds['Distrito'] = dict_encoders['Distrito'].inverse_transform(data_distritos_preds['Distrito'].values.astype(int))
            self.dict_districts_preds[testing_date] = data_distritos_preds.to_dict() #I changed to testing_date

            data_districts_actuals = X_test.groupby('Distrito')[['actuals']].agg('median').reset_index()
            #Calling inverse encoding on Districts.
            data_districts_actuals['Distrito'] = dict_encoders['Distrito'].inverse_transform(data_districts_actuals['Distrito'].values.astype(int))
            self.dict_districts_actuals[testing_date] = data_districts_actuals.to_dict()

            for district in X_test['Distrito'].unique():
                preds_district = X_test[X_test['Distrito']==district]['predictions']
                actuals_district = X_test[X_test['Distrito'] == district]['actuals']
            
                self.dict_districs_metrics[dict_encoders['Distrito'].inverse_transform([int(district)])[0]] = subdict_metrics(actuals_district, preds_district)

            test_year_time = np.datetime_as_string(testing_date).split('-')[0]
            test_month_time = np.datetime_as_string(testing_date).split('-')[1]

            #display(HTML('<p style="text-align:center"> RESULTADOS PARA EL PERIODO {}</p>'.format(
            #    test_year_time + ' - ' + test_month_time)))

            df_temporal_results = pd.DataFrame(self.dict_districs_metrics).T.sort_values(by=['R2'],ascending=False)

            to_append = pd.DataFrame({metric : df_temporal_results[metric].mean() for metric\
                                                     in df_temporal_results.columns},\
                                     index=['Lima_{}_{}'.format(test_year_time,test_month_time)])

            df_temporal_results = df_temporal_results.append(to_append)
            final_metrics_df = final_metrics_df.append(to_append)

        # SAVE RESULTS IN SQLITE DB.

        total_mean = pd.DataFrame({metric : final_metrics_df[metric].mean() for metric\
                                             in final_metrics_df.columns},\
                             index=['TOTAL_MEAN'])
        total_std = pd.DataFrame({metric : final_metrics_df[metric].std() for metric\
                                             in final_metrics_df.columns},\
                             index=['TOTAL_STD'])

        final_metrics_df = final_metrics_df.append(total_mean).append(total_std)
        

            
        