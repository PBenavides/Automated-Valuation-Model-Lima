## Functions to Load, Preprocessing, and Handling Data.
## All the functions here need to be aproved by and documented by notebooks Delivered-*.ipynb


import os, glob, datetime
import logging
import pandas as pd
import numpy as np
import pickle

from sklearn.preprocessing import LabelEncoder
from sklearn.decomposition import PCA

from utils import load_cfg

#In order to use yaml confg file, we'll make this functions.

config = load_cfg('conf.yaml')
conf_preproc = config['Preprocessing']

#Aproved through Experiments - ML Approach - Preprocessing

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
        
class Data_Arima():

    def __init__(self):
        self.uno = 1
    
class Data_VAR():

    def __init__(self):
        self.uno = 1

if __name__ == '__main__':
    data = Data_MlApproach()
    data.save_train_data()

