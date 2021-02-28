import os, glob, datetime
import logging
import pandas as pd
import numpy as np
import pickle

from sklearn.preprocessing import LabelEncoder
from sklearn.decomposition import PCA
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.impute import KNNImputer

def make_dataframe_with_lags(data, start_date, end_date, agg_dictionary, columns_to_pivot, datecol = 'Fecha',
                            index_col='PCA_comp'):
    """
    Pass data and obtain a dataframe with past values as columns, and also a
    Y column to use as a target feature.
    
    I need to:
    Aggregated methods by dictionary.
    From quarter to another.
    With index attached to it.
    """
    
    #The end_date will be use for making the target:
    temp_df = data[(data[datecol] >= start_date)&(data[datecol] < end_date)]
    #standarize columns names
    dict_repl_dates = {elem:'LAG_'+str(n) for n,elem in enumerate(np.sort(temp_df[datecol].unique())[::-1],1)}
    temp_df[datecol].replace(dict_repl_dates, inplace=True)
    #Pivot table for macro data
    macro_lags = pd.pivot_table(temp_df, values=columns_to_pivot, index=index_col, 
                       columns=datecol, aggfunc=agg_dictionary).ffill().bfill().reset_index() #Careful with ffill & bfill
    macro_lags.columns = macro_lags.columns.map('_'.join).str.strip('_')
    #Creating lagged targets:

    lagged_targets = pd.pivot_table(temp_df, values='Precio_m2',index=['PCA_comp','Distrito'], columns='Fecha').reset_index()

    #Creo una dummy para luego reemplazar los lagged_targets
    for lag_col in ['LAG_1','LAG_2','LAG_3','LAG_4']:
        lagged_targets[lag_col+'_isna'] = 0
        lagged_targets[lag_col+'_isna'].iloc[lagged_targets[lagged_targets[lag_col].isna()].index] = 1
    
    X = lagged_targets.iloc[:,:6]
    imputer = KNNImputer(n_neighbors=5)
    imputed_lagged_targets = imputer.fit_transform(X)

    lagged_targets.iloc[:,:6] = pd.DataFrame(imputed_lagged_targets, columns = lagged_targets.iloc[:,:6].columns)
    
    #Actual target. The end_date is my target column.
    main_train = data[data[datecol] == end_date]
    main_target = main_train.groupby(['PCA_comp','Distrito'])['Precio_m2'].median().reset_index().rename(columns={'Precio_m2':'target'})
    #Merge final dataframe
    macro_lagged = macro_lags.merge(lagged_targets, on='PCA_comp',how='left')
    final_df = macro_lagged.merge(main_target, on=['PCA_comp','Distrito'],how='left').dropna()
    
    return final_df

def make_training_dataframe(data, window_size = 60, agg_dictionary = np.mean):
    
    """
    This functions makes the dataframes requiered for training and returns three objects:

    train_data, testing_data, testing_dates_array[-1]; where testing_dates_array is a date array for predicted values.

    train_data has the X_values and the Y_value as a 'target' column.
    ------------------------------------------------------------------------------------------------------------------
    params: 
        - data: The data module as pd.DataFrame object. This has to contain the asummed columns.
        - window_size: The window_size of the periods needed to train. 
        - agg_dictionary: Aggregation method for the summary of time series variables.

    Warning! Preferably rebuild this function!
    """
    
    macroeconomics_indx_col = ['PBI ', 'Ratio adul-joven','TI Trimestral',
                           'CaptBurs Trimestral','INB']
    lista_df = []
    
    #Making train dataset with expanding window approach
    for n in range(0,window_size):
        dates_array = np.sort(data['Fecha'].unique())[n:n+5]
        sample_df = make_dataframe_with_lags(data, start_date = dates_array[0], end_date=dates_array[-1],
                                     agg_dictionary = np.mean,
                                    columns_to_pivot=macroeconomics_indx_col)
        lista_df.append(sample_df)    
    train_data = pd.concat(lista_df).reset_index(drop=True)
    print('TRAIN_DATA: From {} to {}'.format(dates_array[0], dates_array[-1]))
    #Making test dataset with the next period.
    
    testing_dates_array = np.sort(data['Fecha'].unique())[n+1:n+1+5]
    
    assert len(testing_dates_array) == 5
    
    testing_data = make_dataframe_with_lags(data, start_date = testing_dates_array[0], 
                                                end_date = testing_dates_array[-1], agg_dictionary = np.mean,
                                               columns_to_pivot=macroeconomics_indx_col).reset_index(drop=True)

    #print(f'LAST DATE TRAIN:{dates_array[-1]}')
    #print(f'TESTING DATE: {testing_dates_array[-1]}')
    
    return train_data, testing_data, testing_dates_array[-1]

#Formatting data_districts_pred

def formatting_predictions(dict_districts):
    """
    dict_districts: A dictionary with datetime as index, and a subdict with 'Distrito' & 'actuals|predictions'
    This will return us two matrixes, one of predictions and the other of actuals values.
    In order to compare their metrics.
    
    """
    data_districts = pd.DataFrame().from_dict({(outerKey, innerKey) : values for outerKey, innerDict in dict_districts.items() for innerKey, values in innerDict.items()})
    #Duplicate columns
    data_districts.columns = [str(tup[0]) if tup[1] != 'Distrito' else tup[1] for tup in data_districts.columns]
    data_districts = data_districts.loc[:, ~data_districts.columns.duplicated()].set_index('Distrito').T
    data_districts.columns.names = [None]
    
    return data_districts

def calculate_mape(actual, prediction):
        mask = actual != 0
        return (np.fabs(actual - prediction)/actual)[mask].mean()

def subdict_metrics(actuals, preds):
    """
    This function is made to build a dictionary that contains metrics.
    """
    #Calculating metrics:
    mae = mean_absolute_error(actuals, preds)
    mse = mean_squared_error(actuals, preds)
    rmse = np.sqrt(mse)
    rmsle = np.sqrt(np.mean(np.power(np.log(np.array(abs(preds))+1) - np.log(np.array(abs(actuals))+1), 2)))
    r2 = r2_score(actuals,preds)
    mape = calculate_mape(actuals, preds)
    #Since doesn't matter how many time the algorithm will train, we don't add this metrics.
    
    return {'MAE': mae, 'MSE': mse, 'RMSE' : rmse, 'R2' : r2,
                                  'RMSLE' : rmsle, 'MAPE' : mape}


class Data_MlApproach():
    """
    Data Class and Preprocessing Pipeline.

    Here we specify the methods, data files, and considerations to doing dinamycally around the training phase

    --------------------------------------------------------------------------------------------------------------
    file_bcrp:

    file_macro:

    """
    def __init__(self, file_bcrp= './input/BCRP-depas.xlsx', file_macro = './input/macro_data/macro-1999-2019-1.csv'):
        self.data_bcrp = pd.read_excel(file_bcrp)
        self.macro_data = pd.read_csv(file_macro)
        self.prototyping_districts = ['surco', 'miraflores', 'la molina', 'san borja', 'san isidro', 
                         'san miguel', 'magdalena', 'jesús maría', 'pueblo libre', 'lince', 'barranco']


    def data_adjustments(self):
        """
        From the data corrections, transformations and considerations of the dataset.

        """
        #bcrp
        self.data_bcrp['Periodo'] = self.data_bcrp['Año'].astype(str) + '_' + self.data_bcrp['Trimestre'].astype(str)
        self.data_bcrp['Distrito'] = self.data_bcrp['Distrito'].str.lower()
        #macro data
        self.macro_data['Fecha'] = pd.to_datetime(self.macro_data['Fecha'])
        self.data_bcrp = self.data_bcrp.replace('_x00D_','', regex=True)

        #Transform Price and surface to logarithms
        
        df = self.data_bcrp[self.data_bcrp['Distrito'].isin(self.prototyping_districts)]
        df['Precio en soles constantes de 2009'] = np.log(df['Precio en soles constantes de 2009'])
        df['Superficie '] = np.log(df['Superficie '])

        df['Precio_m2'] = df['Precio en soles constantes de 2009']/df['Superficie ']

        #Mapping numeric columns (años de antiguedad) into categories
        df['antiguedad_cat'] = pd.cut(df['Años de antigüedad'], 5, labels=['nuevo','seminuevo','normal','viejo','muy viejo'])

        #Mapping numeric location floor into categories
        df['piso_cat'] = pd.cut(df['Piso de ubicación'], 3, labels=['bajo','medio','alto'])

        #drop erratic data
        df.drop(df[df['Número de habitaciones'] == 0].index,inplace=True)

        df.drop(['Año','Trimestre','Precio en dólares corrientes','Precio en soles corrientes','Precio en soles constantes de 2009'],axis=1, inplace=True)
        #Formatting date time
        df['Periodo']=df['Periodo'].map({x :((pd.to_datetime(x[:4]) + pd.offsets.QuarterEnd(int(x[5:]))) + datetime.timedelta(days=1))\
                                         for x in df['Periodo'].unique()}).dt.floor('D')
        df.rename(columns={'Periodo':'Fecha'},inplace=True)
        #Merge with Macro data:
        to_train = df.merge(self.macro_data, on='Fecha',how='left').dropna()

        #CATEGORIGAL ENCODER:

        dict_encoders = {}
        for col in ['Distrito','antiguedad_cat','piso_cat']:
            #We will keep a record from labelEncoder objects as we'll to inverse_transform the values
            le = LabelEncoder()
            le.fit(to_train[col].values)
            dict_encoders[col] = le
            to_train[col] = le.transform(to_train[col].values)

        #Saving dict_encoders on .pkl file
        with open('./models/objects/dict_encoders.pickle','wb') as handle:
            pickle.dump(dict_encoders, handle, protocol=pickle.HIGHEST_PROTOCOL)

        #Making apartments index with PCA:
        X_to_reduce = to_train[['Número de habitaciones', 'Número de baños','Número de garajes', 'Vista al exterior','piso_cat']]

        #PCA as an index of multiple apartments characteristics.

        pca_1d = PCA(n_components=1)
        values_1d = pca_1d.fit_transform(X_to_reduce)

        print('Shape: {} \n Unique values {}'.format(values_1d.shape, len(np.unique(values_1d))))

        to_train['PCA_comp'] = values_1d

        #Shifting values and transforming to positive ones.
        to_train['PCA_comp'] = to_train['PCA_comp'] + abs(to_train['PCA_comp'].min())
        return to_train

    def save_train_data(self):
        to_train = self.data_adjustments()
        to_train.to_csv('./input/preprocess_data/to_train.csv')
        print('Data is already saved')

    @staticmethod
    def make_encoders_dict(to_train, cols_to_encode):
        """
        Returns a dataframe already encoded and the object dict_encoders
        NOTE: Pls save the maked dict_encoder as object outside the code.
        """
        dict_encoders = {}
        for col in cols_to_encode:
            le = LabelEncoder()
            le.fit(to_train[col].values)
            dict_encoders[col] = le
            to_train[col] = le.transform(to_train[col].values)

        return to_train, dict_encoders